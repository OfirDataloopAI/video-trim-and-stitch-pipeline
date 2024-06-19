import dtlpy as dl
import os
import json


def upload_template(project: dl.Project, app_name: str, template_name: str):
    # Open pipeline template json
    dataloop_json_filepath = os.path.join(os.getcwd(), "dataloop.json")
    with open(dataloop_json_filepath, 'r') as jf:
        dataloop_json_data = json.load(fp=jf)
    dpk = dl.Dpk.from_json(_json=dataloop_json_data, client_api=dl.client_api, project=project)

    # Update pipeline template json data
    dpk.name = app_name
    dpk.display_name = app_name
    template_json_data = dpk.components.pipeline_templates[0]

    template_json_data["name"] = template_name
    template_json_data["projectId"] = project.id
    template_json_data["orgId"] = project.org["id"]
    for template_json_node in template_json_data["nodes"]:
        if template_json_node["namespace"]["projectName"] != "DataloopTasks":
            template_json_node["namespace"]["projectName"] = project.name
        template_json_node["projectId"] = project.id

    # Deploy pipeline template
    dpk = project.dpks.publish(dpk=dpk)
    app = project.apps.install(dpk=dpk)
    print(f"Application ID: {dpk.id}\nInstallation ID: {app.id}")


def main():
    dl.setenv('rc')
    project_id = "098e7068-7c03-4206-8014-27f2a8d0f4bd"
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
