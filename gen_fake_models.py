import os
import random
import shutil


def gen_fake_models():
    base_dir = "models/marts/example"
    directories = [
        "fake1",
        "fake2",
        "fake3",
        "fake4",
        "fake5",
        "fake7",
        "fake8"
    ]

    # uncomment to delete directory if rerunning.
    # if os.path.exists(base_dir):
    #     shutil.rmtree(base_dir)
    #
    # # mkdir
    # os.makedirs(base_dir)

    # create 500 fake SQL files, deleting existing ones before.
    cf = 1
    max_files = 500
    while cf < max_files:
        # pick a random folder name to put this in, from fake1-10, or no folder, which will place
        # it in the root directory
        directory = random.choice(directories + [""])
        dir_name = f"{base_dir}/{directory}"
        file_name = f"fake_{cf}.sql"
        full_path = f"{dir_name}/{file_name}"

        # pick random files to reference that isn't this one
        random_ref = random.choice([i for i in range(1, max_files) if cf != i])

        print(f"{full_path} - ref {random_ref}")
        sql = f"""
        {{{{ config(tags=["fake"], materialized='view') }}}}

        select 1 as foo,
        42 as bar
        from {{{{ ref('fake_{random_ref}') }}}}
        """

        os.makedirs(dir_name, exist_ok=True)

        with open(full_path, "w") as f:
            # basic example to generate random sql so they differ
            f.write(sql)

        cf += 1

if __name__ == "__main__":
    gen_fake_models()