#Simple Script to run chaos cube 
import os, subprocess, signal, time
from time import sleep, time
from pprint import pprint

def main(PINGINTERVAL=1, RUNTIME=1):
    ChaosIntervals = (
        "baseline",
        # "15",
        # "10",
        # "5",
        # "2",
        "1",
    )
    
    RUNTIME = (RUNTIME*10)//PINGINTERVAL
    fullResults = [list() for i in range(len(ChaosIntervals))]

    for test in range(2):
        for interval in ChaosIntervals:
            results = []
            fullResults.append(results)
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
                    results.append(subprocess.check_output("curl -w '%{time_total}' -so /dev/null http://192.168.1.50:8069",shell=True).decode("utf-8")+"\n")
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
            if runCube:
                sleep(30)

    print("Resutlts: ")
    pprint(fullResults)

    for i,v in enumerate(ChaosIntervals):
        fName = f"results/{(int(time()))}-{v}.txt"
        with open(fName,"w") as outFile:
            print(f"Writing results for {fName}")
            for row in zip(*fullResults[i]):
                result = f"{(sum(row)/len(row)):.6f}\n"
                print(result[:-1])
                outFile.write(result)
        print(f"{fName} Written!")

    print("Work complete!")
            
if __name__ == "__main__":
    main()
