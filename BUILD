python_requirements()

docker_image(
    name="mapping-app",
    dependencies=["server/src:app"],
    image_tags=["{build_args.GIT_COMMIT}"]
)
