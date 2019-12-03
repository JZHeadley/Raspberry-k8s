#Simple Script to run chaos cube 
import os, subprocess, signal, time
from time import sleep, time


def main(PINGINTERVAL=1, RUNTIME=1):
    ChaosIntervals = (
        "baseline",
        "15",
        "10",
        "5",
        "2",
        "1",
    )
    
    RUNTIME = (RUNTIME*60)//PINGINTERVAL

    for interval in ChaosIntervals:
        results = []
        runCube = interval != "baseline"
        if runCube:
            startCube = f"docker run --rm --name=chaoskube -v /home/jzheadley/.kube/config:/kube/config quay.io/linki/chaoskube:latest  --kubeconfig=/kube/config --namespaces=default --no-dry-run --interval={interval}s"
            p = subprocess.Popen(startCube.split())
            outMessage = f"Pinging every {PINGINTERVAL} second(s) for {RUNTIME*PINGINTERVAL//60} minute(s) with chaos interval of {interval}s"
        else:
            outMessage = f"Pinging every {PINGINTERVAL} second(s) for {RUNTIME*PINGINTERVAL//60} minute(s)"

        print(outMessage)

        for i in range(RUNTIME):
            print(f"Ping {i+1} of {RUNTIME}")
            try:
                results.append(subprocess.check_output("curl -w '%{time_total}' -so /dev/null http://localhost:8080",shell=True).decode("utf-8")+"\n")
            except Exception as e:
                print("ERROR! "+str(e))
                results.append(str(e)+"\n")
            finally:
                sleep(PINGINTERVAL)

        if runCube:
            os.system("docker kill chaoskube")
            outMessage = f"Ping Test for interval {interval} Done!"
        else:
            outMessage = f"Ping Test for baseline Done!"

        print(outMessage)

        fName = f"{(int(time()))}-{interval}.txt"
        with open(fName,"w") as outFile:
            outFile.writelines(results)
        print("File Written!")
            
    print("Work complete!")
            
if __name__ == "__main__":
    main()
