python_requirements()

docker_image(
    name="mapping-app",
    dependencies=["server/src:app"],
    image_tags=["0.0-{build_args.GIT_COMMIT}"]
)
