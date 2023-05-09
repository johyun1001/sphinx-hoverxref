# Docker 이미지로 Moreh 실행하기

**Hyperscale AI Computing 서비스에서 Docker로 Moreh 실행하는 방법**

Hyperscale AI Computing 서비스는 Docker 컨테이너 안에서 AI 가속기를 사용하는 PyTorch 프로그램을 실행할 수 있도록 전용 Docker 이미지를 제공하고 있습니다. VM에서 다음과 같이 실행하여 AI 가속기가 활성화된 컨테이너를 실행할 수 있습니다.

```shell
(pytorch) ubuntu@vm:~$ sudo moreh-docker-run
...
Login Succeeded
Unable to find image 'sys.deploy.kt-epc.moreh.io:5001/moreh:22.10.2' locally
22.10.2: Pulling from moreh
...
Digest: sha256:b285a30ce74457cc5111b25c7d841f55e9bd090f8ead1a9e79291b7ea03684cc
Status: Downloaded newer image for sys.deploy.kt-epc.moreh.io:5001/moreh:22.10.2
(moreh) root@vm:~#
```

만일, 특정 버전의 Moreh 솔루션 이미지를 실행하고 싶다면, 위 명령어 뒤에 `—-target`이라는 옵션을 추가하여 원하시는 Moreh 솔루션 버전 docker 이미지를 실행하실 수 있습니다. 만일 해당 옵션 없이 `moreh-docker-run`을 실행하면 현재까지 배포된 Moreh 솔루션중 최신 버전으로 이미지를 실행하게 됩니다.

```shell
(pytorch) ubuntu@vm:~$ sudo moreh-docker-run --target 22.10.1
...
https://docs.docker.com/engine/reference/commandline/login/#credentials-store
Login Succeeded
Unable to find image 'sys.deploy.kt-epc.moreh.io:5001/moreh:22.10.1' locally
22.10.1: Pulling from moreh
...
Digest: sha256:fce125f57b7e5ede453c0875e93bf7dfa093b77a64418ecfd970ccf69dd94ae4
Status: Downloaded newer image for sys.deploy.kt-epc.moreh.io:5001/moreh:22.10.1
(moreh) root@moreh-test-vm02:~#
```

컨테이너 안에서 AI 가속기 정보를 조회하고 PyTorch 프로그램을 실행시킬 수 있습니다.

```shell
(moreh) root@vm:~# moreh-smi
+---------------------------------------------------------------------------------------------------+
|  Moreh-SMI 22.10.1                              Client Version: 22.10.1  Server Version: 22.10.2  |
+---------------------------------------------------------------------------------------------------+
|  Device  |        Name         |      Model     |  Memory Usage  |  Total Memory  |  Utilization  |
+===================================================================================================+
|  * 2026  |  KT AI Accelerator  |  Small.64GB  |    22240 MiB   |   131040 MiB   |  -            |
+---------------------------------------------------------------------------------------------------+
Processes:
+----------------------------------------------------------+
|  Device  |  Job ID  |  PID  |  Process  |  Memory Usage  |
+==========================================================+
+----------------------------------------------------------+
(moreh) root@vm:~# python pytorch-sample.py
Downloading http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-images-idx3-ubyte.gz to data/FashionMNIST/raw/train-images-idx3-ubyte.gz
26427392it [00:04, 5389702.34it/s]
Extracting data/FashionMNIST/raw/train-images-idx3-ubyte.gz to data/FashionMNIST/raw
Downloading http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-labels-idx1-ubyte.gz to data/FashionMNIST/raw/train-labels-idx1-ubyte.gz
32768it [00:00, 36542.51it/s]
Extracting data/FashionMNIST/raw/train-labels-idx1-ubyte.gz to data/FashionMNIST/raw
Downloading http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/t10k-images-idx3-ubyte.gz to data/FashionMNIST/raw/t10k-images-idx3-ubyte.gz
4423680it [00:08, 505491.87it/s]
Extracting data/FashionMNIST/raw/t10k-images-idx3-ubyte.gz to data/FashionMNIST/raw
Downloading http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/t10k-labels-idx1-ubyte.gz to data/FashionMNIST/raw/t10k-labels-idx1-ubyte.gz
8192it [00:00, 13945.86it/s]
Extracting data/FashionMNIST/raw/t10k-labels-idx1-ubyte.gz to data/FashionMNIST/raw
Processing...
Done!
[info] Requesting resources for KT AI Accelerator from the server...
[info] Initializing the worker daemon for KT AI Accelerator...
[info] [1/1] Connecting to resources on the server (192.168.00.00:00000)...
[info] Establishing links to the resources...
[info] KT AI Accelerator is ready to use.
Epoch 1
loss: 2.298501  [    0/60000]
loss: 2.287861  [ 6400/60000]
loss: 2.270298  [12800/60000]

```

컨테이너 안에서 인식되는 AI 가속기는 VM에 할당된 AI 가속기와 동일한 것입니다. VM에서 가속기 모델을 변경하면 컨테이너 안에서도 적용되며 그 반대도 마찬가지입니다. 또한 VM에서 AI 가속기를 사용하는 동안은 컨테이너 안에서는 AI 가속기를 사용할 수 없으며 이것 역시 반대도 마찬가지입니다. 예를 들어 VM에서 AI 가속기를 사용하는 train.py 프로그램이 실행 중인 동안 컨테이너에서 AI 가속기를 사용하는 다른 프로그램을 실행할 경우, 아래와 같은 메시지를 출력하고 VM에서 train.py 프로그램이 끝날 때까지 대기하게 됩니다.

```shell
(moreh) root@vm:~# python pytorch-sample.py
...
[info] Requesting resources for KT AI Accelerator from the server...
[warning] KT AI Accelerator is already in use by another process:
[warning]   (pid: 10000) python train.py
[warning] Two or more processes cannot use KT AI Accelerator at the same time. The program will resume automatically after the process 10000 terminates...
```

이 문서의 나머지 부분에서는 Hyperscale AI Computing 서비스를 위한 Docker 컨테이너를 실행하는 과정을(즉, ``moreh-docker-run`` 명령이 내부적으로 하는 일을) 단계별로 자세히 설명합니다.

<aside>
💡 Docker를 사용하지 않고도 VM 안에서 바로 AI 가속기를 사용해 PyTorch 프로그램 실행이 가능합니다. 이 문서는 특별히 Docker 기반으로 실행해야 하는 애플리케이션이 있는 분들을 대상으로 합니다.

</aside>

### 1. 이미지 내려받기

위와 다르게, 단순히 Moreh 솔루션 이미지만 내려받고 싶으시다면 `—-pullonly (-p)` 옵션을 활용하여 이미지를 내려받을수 있습니다.

```shell
(pytorch) ubuntu@vm:~$ sudo moreh-docker-run --pullonly
...
https://docs.docker.com/engine/reference/commandline/login/#credentials-store
Login Succeeded
22.10.2: Pulling from moreh
...
Digest: sha256:b285a30ce74457cc5111b25c7d841f55e9bd090f8ead1a9e79291b7ea03684cc
Status: Downloaded newer image for sys.deploy.kt-epc.moreh.io:5001/moreh:22.10.2
sys.deploy.kt-epc.moreh.io:5001/moreh:22.10.2
```

해당 명령어도 위와 동일하게 만일 특정 버전의 Moreh 솔루션 이미지를 내려받고싶다면, `—-target` 옵션 추가로 이를 수행하실수가 있습니다. 만일 해당 옵션없이 `moreh-docker-run --pullonly`을 실행하면 현재까지 배포된 Moreh 솔루션중 최신 버전으로 이미지를 실행하게 됩니다.

```shell
(pytorch) ubuntu@vm:~$ sudo moreh-docker-run --pullonly --target 22.10.1
...
https://docs.docker.com/engine/reference/commandline/login/#credentials-store
Login Succeeded
22.10.1: Pulling from moreh
...
Digest: sha256:fce125f57b7e5ede453c0875e93bf7dfa093b77a64418ecfd970ccf69dd94ae4
Status: Downloaded newer image for sys.deploy.kt-epc.moreh.io:5001/moreh:22.10.1
sys.deploy.kt-epc.moreh.io:5001/moreh:22.10.1
```

### 2. 컨테이너 시작

다음과 같이 docker run 명령으로 컨테이너를 실행할 수 있습니다. 이 때 다음의 두 가지 옵션을 포함시켜야 합니다.

- **--net=host --privileged**
    - Hyperscale AI Computing 서비스는 GPU와의 빠른 통신을 위해 고속 InfiniBand 네트워크를 사용합니다. --net=host --privileged 옵션은 컨테이너 안에서도 InfiniBand 네트워크에 접속하여 GPU가 위치한 서버와 통신이 가능하도록 합니다. 컨테이너가 실행된 후 ifconfig 명령을 실행하여 ib0 인터페이스가 표시된다면 옵션이 정상적으로 적용된 것입니다.
- **-v /etc/moreh:/etc/moreh**
    - VM의 /etc/moreh 디렉터리에는 AI 가속기 사용 시 resource farm에 접속하기 위한 정보가 저장되어 있습니다. -v /etc/moreh:/etc/moreh 옵션은 컨테이너 안에서도 /etc/moreh 디렉터리에 resource farm 접속 정보가 저장되도록 합니다. 컨테이너가 실행된 후 moreh-smi 명령이 에러 없이 실행된다면 옵션이 정상적으로 적용된 것입니다.

```jsx
(pytorch) ubuntu@vm:~$ sudo docker run --rm -it --net=host --privileged -v /etc/moreh:/etc/moreh sys.deploy.kt-epc.moreh.io:5001/moreh:latest /bin/bash
(moreh) root@vm:~#
```

### 3. Docker Image 실행

**`moreh-docker-run`**

Moreh 솔루션이 담긴 Docker Image를 실행합니다. 추가적으로 다른 옵션값을 안주고 실행했을 경우에는 현재까지 배포된 Moreh 솔루션 이미지중 가장 최신버전 Docker 이미지를 실행하게 됩니다.

**Supported Arguments**

**`--pullonly (-p)`**

해당 옵션값을 추가로 줄경우, Moreh 솔루션 이미지를 바로 실행하지않고 단순히 다운로드 받게 됩니다.

해당 옵션값을 사용할때는 `--target` 옵션값을 추가로 사용 할 수 있으며, `--target`옵션 값 뒤에는 아래 예시 명령어와 같이 버전을 명시해줘야합니다. 만일 없을 경우 최신버전 이미지를 가져오게됩니다.

```shell
(pytorch) ubuntu@vm:~$ sudo moreh-docker-run --pullonly --target 22.10.1
```

**`--version (-v)`**

Moreh 솔루션 Docker Image 버전명을 보여줍니다.



---

Copyright © 2022 Moreh Corporation