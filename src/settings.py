from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "GlaS@MICCAI'2015: Gland Segmentation"
PROJECT_NAME_FULL: str = "GlaS@MICCAI'2015: Gland Segmentation"
HIDE_DATASET = True  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.CC_BY_NC_4_0()
APPLICATIONS: List[Union[Industry, Domain, Research]] = [Industry.Medical(),Research.Medical()]
CATEGORY: Category = Category.Medical()

CV_TASKS: List[CVTask] = [CVTask.InstanceSegmentation(), CVTask.SemanticSegmentation(), CVTask.ObjectDetection()]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.InstanceSegmentation()]

RELEASE_DATE: Optional[str] = None  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = 2015

HOMEPAGE_URL: str = "https://www.kaggle.com/datasets/sani84/glasmiccai2015-gland-segmentation"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 6568253
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/gland-segmentation"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = ["https://www.kaggle.com/datasets/sani84/glasmiccai2015-gland-segmentation"]
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = None
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
# Use dict key to specify name for a button
PAPER: Optional[Union[str, List[str], Dict[str, str]]] = ["https://arxiv.org/abs/1603.00275"]
BLOGPOST: Optional[Union[str, List[str], Dict[str, str]]] = None
REPOSITORY: Optional[Union[str, List[str], Dict[str, str]]] = None

CITATION_URL: Optional[str] = ["https://arxiv.org/abs/1603.00275"]
AUTHORS: Optional[List[str]] = ["Korsuk Sirinukunwattana", "Josien P. W. Pluim", "Hao Chen", "Xiaojuan Qi", "Pheng-Ann Heng", "Yun Bo Guo", "Li Yang Wang", "Bogdan J. Matuszewski", "Elia Bruni", "Urko Sanchez", "Anton Böhm", "Olaf Ronneberger", "Bassem Ben Cheikh", "Daniel Racoceanu", "Philipp Kainz", "Michael Pfeiffer", "Martin Urschler", "David R. J. Snead", "Nasir M. Rajpoot"]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = ["University of Warwick", "Eindhoven University of Technology", "The Chinese University of Hong Kong", "University of Central Lancashire", "University of Freiburg", "ExB Research and Development", "Biomedical Imaging Laboratory (LIB)", "Medical University of Graz", "University of Zurich and ETH Zurich", "Graz University of Technology", "Ludwig Boltzmann Institute for Clinical Forensic Imaging", "University Hospitals Coventry and Warwickshire"]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = ["https://warwick.ac.uk/", "https://www.tue.nl/en/", "https://www.cuhk.edu.hk/", "https://www.uclan.ac.uk/", "https://uni-freiburg.de/en/", "https://exb.de/en/", "https://www.lib.upmc.fr/", "https://www.medunigraz.at/en/", "https://ethz.ch/en.html", "https://www.tugraz.at/en/home/", "https://cfi.lbg.ac.at/en", "https://www.uhcw.nhs.uk/"]

# Set '__PRETEXT__' or '__POSTTEXT__' as a key with string value to add custom text. e.g. SLYTAGSPLIT = {'__POSTTEXT__':'some text}
SLYTAGSPLIT: Optional[Dict[str, Union[List[str], str]]] = {"__POSTTEXT__":"Also, the dataset contains ***patient_id***, ***grade_sirinukunwattana*** and ***malignant***/***benign*** tags"}
TAGS: Optional[List[str]] = None


SECTION_EXPLORE_CUSTOM_DATASETS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "project_name_full": PROJECT_NAME_FULL or PROJECT_NAME,
        "hide_dataset": HIDE_DATASET,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["blog"] = BLOGPOST
    settings["repository"] = REPOSITORY
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings
