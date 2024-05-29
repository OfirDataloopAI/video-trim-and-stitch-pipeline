import dtlpy as dl
import os
import json


def upload_template(project: dl.Project, app_name: str, template_name: str):
    # Open pipeline template json
    dataloop_json_filepath = os.path.join(os.getcwd(), "dataloop.json")
    with open(dataloop_json_filepath, 'r') as jf:
        dataloop_json_data = json.load(fp=jf)

    # Update pipeline template json data
    dataloop_json_data["name"] = app_name
    dataloop_json_data["displayName"] = app_name

    template_json_data = dataloop_json_data["components"]["pipelineTemplates"][0]
    template_json_data["name"] = template_name
    template_json_data["projectId"] = project.id
    template_json_data["orgId"] = project.org["id"]
    for template_json_node in template_json_data["nodes"]:
        if template_json_node["namespace"]["projectName"] != "DataloopTasks":
            template_json_node["namespace"]["projectName"] = project.name
        template_json_node["projectId"] = project.id

    # Overwrite pipeline template json data
    with open(dataloop_json_filepath, 'w') as jf:
        json.dump(obj=dataloop_json_data, fp=jf, indent=4)

    # Deploy pipeline template
    dpk = project.dpks.publish()
    app = project.apps.install(dpk=dpk)
    print(
        f"Application ID: {dpk.id}\n"
        f"Installation ID: {app.id}"
    )


def main():
    dl.setenv('rc')
    project_id = "bb731b48-ae1a-45b9-8e60-4a62022090de"
    app_name = "video-trim-and-stitch-pipeline"
    template_name = "vts-pipeline"

    project = dl.projects.get(project_id=project_id)
    app_name = f"{app_name}-{project.name}"
    upload_template(
        project=project,
        app_name=app_name,
        template_name=template_name
    )


if __name__ == '__main__':
    main()
