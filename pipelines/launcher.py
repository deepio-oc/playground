import kfp

def pipelines_laucher(pipelines_str, experiment_name):
    import kfp, os, datetime, json

    client = kfp.Client()
    pipelines = json.loads(pipelines_str)

    experiment = client.create_experiment(name=experiment_name)

    for pipeline_name in pipelines:
        pipeline_id = client.get_pipeline_id(pipeline_name)
        run_name = pipeline_name + " " + datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        run_info = client.run_pipeline(experiment.id, run_name, pipeline_id=pipeline_id)
        print (f"{pipeline_name} run: {run_name}")
        
        response = client.wait_for_run_completion(run_info.id, 60*60) #1 hour wait period
        print (f"{pipeline_name} finished with status: {response.run.status}")
        
        assert response.run.status.lower() in ["succeeded","skipped"], f"{pipeline_name} failed"

launcher_op = kfp.components.create_component_from_func(pipelines_laucher, base_image="ocdr/kfpsdk")


@kfp.dsl.pipeline(name="Pipelines launcher", description="Launch list of pipelines")
def launcher_pipeline(pipelines, experiment_name='Default'):
    launcher_op (pipelines, experiment_name)


kfp.compiler.Compiler().compile(launcher_pipeline, "pipelines_launcher.zip")