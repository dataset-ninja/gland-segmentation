Dataset **GlaS@MICCAI'2015: Gland Segmentation** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzIzNjhfR2xhU0BNSUNDQUknMjAxNTogR2xhbmQgU2VnbWVudGF0aW9uL2dsYXNAbWljY2FpJzIwMTU6LWdsYW5kLXNlZ21lbnRhdGlvbi1EYXRhc2V0TmluamEudGFyIiwgInNpZyI6ICJ4TjlXTFVZTStjbFNpOEZ4KzlXUzNWTzlFK1gvcWV2UThrSFZST1Jwd0F3PSJ9)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='GlaS@MICCAI'2015: Gland Segmentation', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.kaggle.com/datasets/sani84/glasmiccai2015-gland-segmentation).