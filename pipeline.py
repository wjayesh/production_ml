from kubernetes import client as k8s_client
import kfp.dsl as dsl
import kfp.compiler as compiler
import kfp.components as components
import kfp

@dsl.pipeline(
    name='Azure prod pipeline',
    description='sample pipeline'
)
def sample_pipeline(
    persistent_volume_path='/mnt/azure',
    training_folder='train',
    training_dataset='train.csv',
    model_folder='model',
    export_bucket='model-bucket'
):
    """Pipeline steps"""

    # fetch data
    operations['fetch'] = dsl.ContainerOp(
        name='fetch',
        image='<image name:tag>',
        command=['python3'],
        arguments=[
            '/scripts/fetch_from_source.py',
            '--base_path', persistent_volume_path,
            '--data', training_folder,
            '--target', training_dataset,
        ]
    )

    # train
    operations['training'] = dsl.ContainerOp(
        name='training',
        image='<image name:tag>',
        command=['python3'],
        arguments=[
            '/scripts/code/run.py',
            '--base_path', persistent_volume_path,
            '--data', training_folder,
            '--outputs', model_folder,
        ]
    )
    operations['training'].after(operations['fetch'])

    # export model
    operations['export'] = dsl.ContainerOp(
        name='export',
        image='<image name:tag>',
        command=['python3'],
        arguments=[
            '/scripts/export_to_s3.py',
            '--base_path', persistent_volume_path,
            '--model', 'model',
            '--s3_bucket', export_bucket
        ]
    )
    operations['export'].after(operations['training'])

    kfserving = components.load_component_from_file(
        '/serve/kfserving-component.yaml')

    operations['serving'] = kfserving(
        action="apply",
        default_model_uri=f"s3://{export_bucket}/model_latest.h5",
        model_name="sample_model",
        framework="tensorflow",
    )
    operations['serving'].after(operations['export'])
    
  for _, op_1 in operations.items():
    op_1.container.set_image_pull_policy("Always")
    op_1.add_volume(
      k8s_client.V1Volume(
        name='azure',
        persistent_volume_claim=k8s_client.V1PersistentVolumeClaimVolumeSource(
          claim_name='azure-disk')
      )
    ).add_volume_mount(k8s_client.V1VolumeMount(
      mount_path='/mnt/azure', name='azure'))

# comment these lines when using notebook
if __name__ == '__main__':
  import kfp.compiler as compiler
  compiler.Compiler().compile('sample_pipeline', __file__ + '.tar.gz')


## Uncomment when running code in notebook
  # client = kfp.Client()
  # run_result = client.create_run_from_pipeline_func(
  #     pipeline_func=sample_pipeline,
  #     experiment_name='experiment_name',
  #     run_name='run_name',
  #     arguments='arguments',
  # )
