import csv
import numpy as np
import supervisely as sly
import os
from dataset_tools.convert import unpack_if_archive
import src.settings as s
from urllib.parse import unquote, urlparse
from supervisely.io.fs import get_file_name, get_file_size
import shutil

from tqdm import tqdm

def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:        
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path
    
def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count
    
def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    dataset_path = "Warwick_QU_Dataset"
    tags_path = os.path.join("Warwick_QU_Dataset","Grade.csv")
    batch_size = 30
    masks_suffix = "_anno.bmp"


    def create_ann(image_path):
        labels = []

        image_name = get_file_name(image_path)

        tags_data = im_name_to_tags[image_name]
        patient_id = sly.Tag(tag_id, value=int(tags_data[0]))
        glas = tags_data[1]
        if "benign" in glas:
            glas = sly.Tag(tag_benign)
        elif "malignant" in glas:
            glas = sly.Tag(tag_malignant)
        sirinukunwattana = sly.Tag(tag_sirinukunwattana, value=tags_data[2])
        mask_path = os.path.join(dataset_path, image_name + masks_suffix)
        mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
        img_height = mask_np.shape[0]
        img_wight = mask_np.shape[1]
        unique_pixels = np.unique(mask_np)[1:]
        for pixel in unique_pixels:
            mask = mask_np == pixel
            curr_bitmap = sly.Bitmap(mask)
            curr_label = sly.Label(curr_bitmap, obj_class)
            labels.append(curr_label)

        return sly.Annotation(
            img_size=(img_height, img_wight),
            labels=labels,
            img_tags=[patient_id, glas, sirinukunwattana],
        )


    obj_class = sly.ObjClass("gland", sly.Bitmap)

    tag_id = sly.TagMeta("patient_id", sly.TagValueType.ANY_NUMBER)
    tag_malignant = sly.TagMeta("malignant", sly.TagValueType.NONE)
    tag_benign = sly.TagMeta("benign", sly.TagValueType.NONE)
    tag_sirinukunwattana = sly.TagMeta("grade_sirinukunwattana", sly.TagValueType.ANY_STRING)


    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=[obj_class],
        tag_metas=[tag_id, tag_malignant, tag_benign, tag_sirinukunwattana],
    )
    api.project.update_meta(project.id, meta.to_json())

    im_name_to_tags = {}
    with open(tags_path, "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            im_name_to_tags[row[0]] = row[1:]

    train_images_names = [
        im_name
        for im_name in os.listdir(dataset_path)
        if im_name[:5] == "train" and len(im_name.split("_")) == 2
    ]

    test_A_images_names = [
        im_name
        for im_name in os.listdir(dataset_path)
        if im_name[:5] == "testA" and len(im_name.split("_")) == 2
    ]

    test_B_images_names = [
        im_name
        for im_name in os.listdir(dataset_path)
        if im_name[:5] == "testB" and len(im_name.split("_")) == 2
    ]

    ds_name_to_images_names = {"train": train_images_names, "test_a": test_A_images_names, "test_b": test_B_images_names}

    for ds_name, images_names in ds_name_to_images_names.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for img_names_batch in sly.batched(images_names, batch_size=batch_size):
            images_pathes_batch = [
                os.path.join(dataset_path, image_name) for image_name in img_names_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, images_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns_batch = [create_ann(image_path) for image_path in images_pathes_batch]
            api.annotation.upload_anns(img_ids, anns_batch)

            progress.iters_done_report(len(img_names_batch))
    
    return project
