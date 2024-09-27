from prefect import task, Flow
import subprocess

#prefect server file
#to run
#prefect server start --> start server
#python prefect_server.py --> register flow
#prefect agent local start --> start a local agent for monitoring


#alternativly run via prefects cloud registration using (requires api)
#prefect agent start -q 'default'

schedule = IntervalSchedule(interval=timedelta(weeks=2)) #interval 2 weeks can change


@task
def run_grab():
    try:
        subprocess.run(['python', '/Users/jye/Desktop/scrape_v2/scripts/grab_links.py'], check=True)
        print("grab_links.py executed.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing grab_links.py: {e}")


@task
def run_scrape():
    try: 
        subprocess.run(['python', '/Users/jye/Desktop/scrape_v2/scripts/scrape.py'], check=True)
        print("scrape.py executed.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing scrape.py: {e}")


@task
def run_summarize():
    try: 
        subprocess.run(['python', '/Users/jye/Desktop/scrape_v2/scripts/generate_summaries.py'], check=True)
        print("generate_summaries.py executed.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing generate_summaries.py: {e}")


@task
def run_bullet_points():
    try: 
        subprocess.run(['python', '/Users/jye/Desktop/scrape_v2/scripts/generate_bullet_points.py'], check=True)
        print("generate_bullet_points.py executed.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing generate_bullet_points.py: {e}")

@task
def run_stop_words():
    try: 
        subprocess.run(['python', '/Users/jye/Desktop/scrape_v2/scripts/remove_stop_words.py'], check=True)
        print("remove_stop_words.py executed.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing remove_stop_words.py: {e}")


with Flow("run-scripts-flow", schedule = schedule) as flow:

    scrape = run_scrape()
    grab = run_grab()
    summarize = run_summarize()
    bullet_points = run_bullet_points()
    stop = run_stop_words()



    scrape.set_upstream(grab)
    summarize.set_upstream(scrape)
    bullet_points.set_upstream(summarize) #ensure order
    run.set_upstream(bullet_points)


# if __name__ == "__main__":
#     flow.run()
# ^ for local 

#flow.register(project_name="gsc") #grab, scrape, clean --> for cloud
# prefect cloud login --> login to cloud

#one option or the other