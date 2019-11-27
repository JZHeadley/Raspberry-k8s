#Simple Script to run chaos cube 
import os, subprocess, signal, time
from time import sleep, time


def main(PINGINTERVAL=2, RUNTIME=1):
    ChaosIntervals = (
        "15",
        "10",
        "5",
        "2",
        "1"
    )
    
    RUNTIME = (RUNTIME*60)//PINGINTERVAL

    for interval in ChaosIntervals:
        results = []
        startCube = f"docker run --name=chaoskube -v ~/.kube/config:/kube/config quay.io/linki/chaoskube:latest  --kubeconfig=/kube/config --namespaces=default --no-dry-run --interval={interval}s"
        p = subprocess.Popen(startCube.split())
        
        for i in range(RUNTIME):
            results.append(float(os.system("ping -c 1 http://localhost:9090"))/1000)
            sleep(PINGInterval)

        os.system("docker kill chaoskube")

        with open(f"{(int(time())}-{interval}.txt","w") as outFile:
            outFile.writelines(results)
            
            
if __name__ == "__main__":
    main()
