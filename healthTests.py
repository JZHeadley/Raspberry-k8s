#Simple Script to run chaos cube 
import os, subprocess, signal, time
from time import sleep, time
from pprint import pprint

def main(PINGINTERVAL=1, RUNTIME=10, RUNS=3):
    ChaosIntervals = (
        "baseline",
        # "15",
        # "10",
        # "5",
        # "2",
        "1",
    )
    
    RUNTIME = RUNTIME//PINGINTERVAL

    for interval in ChaosIntervals:
        fullSet = []
        for i in range(RUNS):
            results = []
            fullSet.append(results)
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
                    results.append(float(subprocess.check_output("curl -w '%{time_total}' -so /dev/null http://192.168.1.50:8069",shell=True).decode("utf-8")))
                except Exception as e:
                    print("ERROR! "+str(e))
                    results.append(2.0)
                finally:
                    sleep(PINGINTERVAL)

            if runCube:
                os.system("docker kill chaoskube")
                outMessage = f"Ping Test for interval {interval} Done!"
            else:
                outMessage = f"Ping Test for baseline Done!"

            print(outMessage)
            if runCube:
                sleep(30)

        fName = f"results/{(int(time()))}-{interval}.txt"
        with open(fName,"w") as outFile:
            for row in zip(*fullSet):
                outFile.write(f"{(sum(row)/len(row)):.6f}\n")
        print(f"{fName} Written!")

    print("Work complete!")
            
if __name__ == "__main__":
    main()
