
Error FAQ
=========

이 문서는 `트러블슈팅 <https://moreh-corporation-moreh-test-search.readthedocs-hosted.com/ko/latest/HAC/%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85.html>`_ 과 같이 HAC 서비스 사용자를 위해 오류 해결 방안을 제공합니다. 이 페이지의 해결 가이드대로 진행했음에도 같은 문제가 발생하거나 현재 발생하는 에러코드 및 메시지를 이 페이지에서 찾지 못하실 경우에는 고객지원을 요청해 주시기 바랍니다.


VM / 환경 관련 
~~~~~~~~~~~~

Q. VM에서 update-moreh 가 안됩니다.
-------------------------------

**A.** ``update-moreh --force --tensorflow`` 시 아래와 같이 update가 진행되지 않거나 아래와 같은 에러케이스가 발생하면 .local 이슈로 인한 문제일 수 있습니다. 해당 폴더 ~/.local/lib, ~/.local/bin 을 삭제 후 재시도해보시기 바랍니다.

* curl 명령어 이상으로 update-moreh가 안되는 경우

   .. code-block:: bash
  
      (pytorch) ubuntu@vm:~$ update-moreh --force --tensorflow
      ...
      /home/ubuntu/.conda/envs/${CONDA_ENV}/lib/libtinfo.so.6: no version information available (required by bash)
      Warning:Tensorflow 2.9.0, Pytorch > 1.7.1 can operate only for users whose experimental version has been confirmed.
      Do you want to proceed? (Press any key to proceed)
      curl: symbol lookup error: /lib/x86_64-linux-gnu/libp11-kit.so.0: undefined symbol: ffi_type_pointer, version LIBFFI_BASE_7.0
      Moreh AI Platform is not available.
      Latest Version is

* tensorflow 패키지가 다른 환경에 설치되는 경우
  
   .. code-block:: bash
    
      (pytorch) ubuntu@vm:~$ update-moreh --force --tensorflow
      ...
      Start removing Moreh hookings.
      Traceback (most recent call last):
      File "remove_tf_keras_hook.py", line 112, in <module>
      main()
      File "remove_tf_keras_hook.py", line 96, in main
      raise RuntimeError('TensorFlow is not installed.')
      RuntimeError: TensorFlow is not installed.



Q. VM에서 lspci 혹은 nvidia-smi를 실행했는데 GPU가 인식이 되지 않습니다.
--------------------------------------------------------------

**A.** AI 가속기 정보는 터미널에서 ``moreh-smi`` 명령을 실행하여 확인할 수 있습니다. "KT AI Accelerator" 디바이스가 하나 표시되면 정상적으로 AI 가속기가 할당되어 있는 것입니다.

.. code-block:: shell

    (pytorch) ubuntu@vm:~$ moreh-smi
    +--------------------------------------------------------------------------------------------------------------+
    |                                                                Current Version: 0.8.0  Latest Version: 0.8.0  |
    +--------------------------------------------------------------------------------------------------------------+
    |  Device  |        Name         |            Token           |     Model    |  Memory Usage  |  Total Memory  |
    +==============================================================================================================+
    |       1  |  KT AI Accelerator  |  ZXhhbXBsZSB0b2tlbiBzdHI=  |  Small.16GB  |  -             |  -             |
    +--------------------------------------------------------------------------------------------------------------+

    Processes:
    +----------------------------------------------------------+
    |  Device  |  Job ID  |  PID  |  Process  |  Memory Usage  |
    +==========================================================+
    +----------------------------------------------------------+


.. code-block:: shell

    (pytorch) ubuntu@vm:~$ moreh-smi
    +--------------------------------------------------------------------------------------------------------------+
    |                                                               Current Version: 0.8.0  Latest Version: 0.8.0  |
    +--------------------------------------------------------------------------------------------------------------+
    |  Device  |        Name         |            Token           |     Model    |  Memory Usage  |  Total Memory  |
    +==============================================================================================================+
    |       1  |  KT AI Accelerator  |  ZXhhbXBsZSB0b2tlbiBzdHI=  |  Small.16GB  |  -             |  -             |
    +--------------------------------------------------------------------------------------------------------------+

    Processes:
    +----------------------------------------------------------+
    |  Device  |  Job ID  |  PID  |  Process  |  Memory Usage  |
    +==========================================================+
    +----------------------------------------------------------+


AI 가속기는 PyTorch에서 `cuda:0` 디바이스로 인식되며, 기존 CUDA 디바이스와 호환되는 API를 제공합니다. 따라서 물리적인 GPU가 없더라도 기존에 NVIDIA GPU용으로 작성된 PyTorch 프로그램을 그대로 실행할 수 있습니다.


Q. VM 로그인 시 기본적으로 “pytorch”라는 Anaconda 가상 환경이 활성화됩니다. 다른 가상 환경을 만들 수는 없습니까?
---------------------------------------------------------------------------------------------

A. “pytorch” 가상 환경에는 이미 Hyperscale AI Computing 서비스를 위한 각종 소프트웨어 설정이 완료되어 있으므로 가급적 해당 환경에서 시스템을 사용해 주시기를 권장 드립니다.

만약 별도의 가상 환경을 생성하기를 희망하실 경우, Python 3.8 버전을 사용하도록 가상 환경을 만들어 주시고 ``update-moreh --target`` 명령을 사용하여 해당 가상 환경 내에서 최신 버전의 Hyperscale AI Computing 서비스용 PyTorch를 재설치하시기 바랍니다.

.. code-block:: shell

    (base) ubuntu@vm:~$ conda create -n your_new_env python=3.8 
    (base) ubuntu@vm:~$ conda activate your_new_env
    (your_new_env) ubuntu@vm:~$ update-moreh --target (latest version)

여러 개의 가상 환경에서 동시에 AI 가속기를 사용하시려는 경우 반드시 모든 가상 환경에서 동일 버전의 PyTorch가 설치되어 있어야 합니다. 각 가상 환경에서 차례로 ``update-moreh`` 명령을 실행하여 최신 버전의 소프트웨어를 설치할 수 있습니다.


Q. 특정 VM에서 update-moreh, moreh-smi 등 작업이 정상적으로 이뤄지지 않습니다.
--------------------------------------------------------------------------------------

A. IB 포트에서 IP를 할당받지 못하는 경우는 IB 포트명이 golden image 설정할 때와 다른 상태로 변경되었을 가능성이 있습니다. (shelve/unshelve 등으로 IB포트의 PCI bus number 변경이 된 경우). 이 경우 IB 포트의 dhcp 설정에 문제가 발생합니다.
``ifconfig | grep -A1 ibs`` 에서 인터페이스명이 ibs5가 아닌 다른 이름으로 (ex. ibs6) 변경됨이 확인된 경우 아래 조치를 취하시기 바랍니다.

VM 부팅 단계에서 IB 인터페이스를 인식하여 dhcp 및 Moreh UCX통신할 수 있게 설정을 변경하는 작업입니다.

  1. 아래 Script를 /etc/moreh 에 작성하십시오. (``set_interface.sh``) 이때 ``/bin/bash /etc/moreh/set_interface.sh`` 로 직접 스크립트 1회 실행시켜야 합니다
  
  .. code-block:: shell

    #!/bin/bash

    DESCRIPTION="MT28908 Family"
    INTERFACE_FILE="/etc/network/interfaces"
    MOREH_FILE="/etc/moreh/net_interfaces"
    INTERFACE_NAME=""

    lshw_output=$(lshw -C network -short)

    while read -r line; do
      if [[ "$line" == *"$DESCRIPTION"* ]]; then
        INTERFACE_NAME=$(echo "$line" | awk '{print $2}')
        break
      fi
    done <<< "$lshw_output"

    if [[ -z "$INTERFACE_NAME" ]]; then
      echo "Error: Could not find interface with description $DESCRIPTION"
      exit 1
    fi

    echo "auto $INTERFACE_NAME" > $INTERFACE_FILE
    echo "iface $INTERFACE_NAME inet dhcp" >> $INTERFACE_FILE
    echo "$INTERFACE_NAME" > $MOREH_FILE

    systemctl restart networking

  2. 위 1번이 적용된 이후 다음 재 부팅 시 Cron을 이용한 부팅으로 아래 스크립트가 실행되게끔 설정하십시오.
  
  Cron이란 리눅스(Linux) 계열에서 특정 시간에 특정 작업을 하는 데몬을 의미하며 이를 수행하도록 명령 리스트를 만드는 것이 아래와 같은 Crontab 설정 작업입니다.
 
  * Cron 설정하기
  
    .. code-block:: shell

      # Crontab 편집
      crontab -e
      @reboot sleep 10 && /bin/bash /etc/moreh/set_interface.sh



학습 실행 관련 (Pytorch)
~~~~~~~~~~~~~~~~~~~~~

Q. 에러현상: `version GLIBC_2.29' not found 관련 이슈가 뜹니다.
---------------------------------------------------------

  .. code-block:: shell
    
    ImportError: /lib/x86_64-linux-gnu/libm.so.6: version 'GLIBC_2.29' not found (required by /home/ubuntu/.conda/envs/pytorch/lib/python3.8/site-packages/moreh/driver/pytorch/moreh_module/_moreh_f.so)

**A.** 고객의 VM이 Ubuntu 18.04 또는 그 이하의 VM으로 생성될 경우 발생하는 문제일 수 있습니다. 해당 고객의 VM을 Ubuntu 20.04 로 생성 바랍니다.


Q. PyTorch 프로그램을 실행하였는데 "Two or more processes cannot use KT AI Accelerator at the same time." 메시지가 출력되고 프로그램이 멈춰 있습니다.
------------------------------------------------------------------------------------------------------------------------------------

**A.** Hyperscale AI Computing 서비스는 하나의 VM에서 AI 가속기를 사용하는 프로그램을 동시에 두 개 이상 실행할 수 없도록 되어 있습니다. 따라서 예를 들어 AI 가속기를 사용하는 train.py 프로그램이 실행 중인 동안 마찬가지로 AI 가속기를 사용하는 inference.py 프로그램을 실행할 경우, 나중에 실행한 프로그램은 메시지를 출력하고 앞에 실행한 프로그램이 끝날 때까지 대기하게 됩니다.

.. code-block:: shell

    (pytorch) ubuntu@vm:~$ python inference.py
    ...
    [info] Requesting resources for KT AI Accelerator from the server...
    [warning] KT AI Accelerator is already in use by another process:
    [warning]   (pid: 10000) python train.py
    [warning] Two or more processes cannot use KT AI Accelerator at the same time. The program will resume automatically after the process 10000 terminates...

만약 AI 가속기를 사용하는 다른 프로그램이 없는데도 위와 같은 메시지가 표시된다면 다음 질문을 참고하십시오.


Q. VM에서 실행 중인 다른 PyTorch 프로그램이 없음에도 불구하고 계속 "Two or more processes cannot use KT AI Accelerator at the same time." 메시지가 출력됩니다.
--------------------------------------------------------------------------------------------------------------------------------------------

**A.** 일부 PyTorch 프로그램은 학습/추론 과정에서 데이터를 빠르게 불러 오기 위해 별도의 DataLoader 프로세스를 실행합니다. 이 경우 PyTorch 프로그램이 비정상 종료했을 때(예를 들어 Ctrl+C로 강제 종료했을 때) 주 프로세스는 없어지더라도 DataLoader 프로세스는 없어지지 않고 AI 가속기와 CPU 코어, 메인 메모리를 점유하면서 남아 있는 경우가 있습니다.

현재 VM에 실행 중인 Python 프로세스가 존재하는지 ``ps aux | grep python`` 명령으로 확인할 수 있습니다. 또한 실행 중인 모든 Python 프로세스를 pkill python 명령으로 제거할 수 있습니다.

.. code-block:: shell

    (pytorch) ubuntu@vm:~$ ps aux | grep python
    root      1700  0.0  0.0 169104 17136 ?        Ssl  Dec03   0:00 /usr/bin/python3 /usr/bin/networkd-dispatcher --run-startup-triggers
    root      1900  0.0  0.0 185956 20112 ?        Ssl  Dec03   0:00 /usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-signal
    ubuntu    9900 84.1  0.1 3688828 508348 pts/1  Sl   08:50   0:18 python train.py
    ubuntu    9901 79.5  0.1 3671492 491104 pts/1  Sl   08:50   0:17 python train.py
    ubuntu    9902 65.4  0.1 3670744 490580 pts/1  Sl   08:50   0:14 python train.py
    ubuntu    9903 67.5  0.1 3671280 490440 pts/1  Sl   08:50   0:14 python train.py
    ubuntu   10000  0.0  0.0  14864  1116 pts/2    S+   08:51   0:00 grep --color=auto python
    (pytorch) ubuntu@vm:~$ pkill python
    (pytorch) ubuntu@vm:~$ ps aux | grep python*
    root      1700  0.0  0.0 169104 17136 ?        Ssl  Dec03   0:00 /usr/bin/python3 /usr/bin/networkd-dispatcher --run-startup-triggers
    root      1900  0.0  0.0 185956 20112 ?        Ssl  Dec03   0:00 /usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-signal
    ubuntu   10001  0.0  0.0  14864  1116 pts/2    S+   08:51   0:00 grep --color=auto python

만약 실행 중인 Python 프로세스가 전혀 존재하지 않음에도 불구하고 위와 같은 메시지가 표시된다면 ``moreh-smi --reset`` 명령으로 GPU 자원을 강제로 할당 해제할 수 있습니다.

.. code-block:: shell

    (pytorch) ubuntu@vm:~$ moreh-smi --reset
    Device release success.

이 두 가지 방법으로도 문제가 해결되지 않으면 기술 지원을 받으시기 바랍니다.



Q. PyTorch 프로그램을 실행하였는데 "Not enough resources are currently available for KT AI Accelerator." 메시지가 출력되고 프로그램이 멈춰 있습니다.
-----------------------------------------------------------------------------------------------------------------------------------

**A.** Hyperscale AI Computing 시스템에 동시에 너무 많은 자원 할당 요청이 들어 올 경우 일시적으로 GPU 자원의 신규 할당이 불가능할 수 있습니다. 이 경우 프로그램이 메시지를 출력하고 GPU 자원이 할당될 때까지 대기할 수 있습니다. 이 경우 가만히 있으면 GPU 자원을 할당 받은 이후 자동으로 실행이 재개됩니다.

.. code-block:: shell

    (pytorch) ubuntu@vm:~$ python train.py
    ...
    [info] Requesting resources for KT AI Accelerator from the server...
    [warning] Not enough resources are currently available for KT AI Accelerator. All resources in the system are being used by other users. The program will resume automatically when resources become available...



Q. PyTorch 프로그램을 실행하였는데 "The current version of Moreh AI Framework is outdated and no longer supported in the system" 메시지가 출력되고 프로그램이 강제 종료됩니다.
-------------------------------------------------------------------------------------------------------------------------------------------------------------

**A.** Hyperscale AI Computing 서비스는 지속적으로 소프트웨어 업데이트가 이루어지고 있습니다. 현재 VM에 설치된 소프트웨어가 구 버전인 경우 실제 GPU 쪽 소프트웨어와 호환성이 맞지 않아 프로그램 실행이 불가능할 수 있습니다. 이 경우 터미널에서 ``update-moreh`` 명령을 실행하여 소프트웨어를 자동으로 업데이트할 수 있습니다.

.. code-block:: shell

    (pytorch) ubuntu@vm:~$ update-moreh
    Currently installed: 0.8.0
    Possible upgrading version: 0.8.1

    Do you want to upgrade? (y/n, default:n)
    y
    ...
    Finished processing dependencies for moreh-driver==0.8.1

    installed : /usr/bin/moreh-smi
    installed : /usr/bin/moreh-switch-model
    installed : /usr/bin/update-moreh
    installed : /usr/lib/libcommunication.so
    installed : /usr/lib/libmodnnruntime.so


Q. PyTorch 프로그램을 실행하였는데 CUDA error가 출력되면서 프로그램이 강제 종료됩니다.
----------------------------------------------------------------------

**A.** 우선 터미널에서 conda list pytorch를 실행하여 PyTorch가 정상 설치되었는지 확인하십시오. PyTorch 버전이 1.7.1+cu110.moreh00.0.0와 같은 형식으로 표시되면 정상 설치되어 있는 것입니다.

.. code-block:: shell

    (pytorch) ubuntu@vm:~$ conda list torch
    # packages in environment at /home/ubuntu/.conda/envs/pytorch:
    #
    # Name                    Version                   Build  Channel
    torch                     1.7.1+cu110.moreh22.8.0          pypi_0    pypi
    torchaudio                0.7.2                    pypi_0    pypi
    torchvision               0.8.2                    pypi_0    pypi

그리고 다음과 같이 실행하여 PyTorch 버전 및 Hyperscale AI Computing 플러그인 버전 정보를 확인하십시오. import torch 혹은 torch.version.moreh 결과 에러가 발생하면 PyTorch 혹은 플러그인에 문제가 있는 것입니다.

.. code-block:: shell

    (pytorch) ubuntu@vm:~$ python
    Python 3.8.12 (default, Oct 12 2021, 13:49:34)
    [GCC 7.5.0] :: Anaconda, Inc. on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import torch
    >>> torch.__version__
    '1.7.1'
    >>> torch.version.moreh
    '22.8.0'
    >>> quit()
    (pytorch) ubuntu@vm:~$


위 두 단계 중 하나에서 실패한 경우 다음과 같이 실행하여 PyTorch를 재설치해 보십시오.

.. code-block:: shell

    (pytorch) ubuntu@vm:~$ update-moreh --force


애플리케이션에 NVIDIA GPU 의존적인 기능이 포함되어 있는 경우 Hyperscale AI Computing 서비스용 PyTorch가 정상 설치되었더라도 CUDA error가 발생할 수 있습니다. 이 경우 별도로 기술 지원을 받으시기 바랍니다.



Q. PyTorch 프로그램을 실행하거나 update-moreh 명령을 실행할 때 "ImportError: numpy.core.multiarray failed to import" 에러가 발생합니다.
-------------------------------------------------------------------------------------------------------------------------

**A.** 시스템에 너무 낮은 버전(1.16 미만)의 NumPy 라이브러리가 설치되어 문제가 발생할 수 있습니다. 다음과 같이 실행하여 현재 설치된 NumPy 버전을 확인하십시오.

.. code-block:: shell

    (pytorch) ubuntu@vm:~$ conda list numpy
    # packages in environment at /home/ubuntu/.conda/envs/pytorch:
    #
    # Name                    Version                   Build  Channel
    numpy                     1.15.2                   pypi_0    pypi

다음과 같이 실행하여 NumPy 버전을 업데이트할 수 있습니다.

.. code-block:: shell

    (pytorch) ubuntu@vm:~$ conda install numpy -c conda-forge




Q. PyTorch 프로그램을 실행하거나 moreh-smi 혹은 moreh-switch-model 명령을 실행하였는데 "SDA token is not given." 에러가 발생합니다.
------------------------------------------------------------------------------------------------------------------

**A.** Hyperscale AI Computing 서비스는 AI 가속기를 식별하기 위해 /etc/moreh/token 파일의 내용을 읽어 옵니다. 다음과 같이 실행하여 해당 파일이 접근 가능한지 확인하십시오.

.. code-block:: shell

    (pytorch) ubuntu@vm:~$ cat /etc/moreh/token
    ZXhhbXBsZSB0b2tlbiBzdHI=


만약 위와 같이 실행하였을 때 문제가 발생한다면 기술 지원을 받으시기 바랍니다.


Q. moreh-switch-model 명령으로 AI 가속기 모델을 바꾸려고 하니 "The model cannot be switched while the KT AI Accelerator is in use." 에러가 발생합니다.
-----------------------------------------------------------------------------------------------------------------------------------------

**A.** AI 가속기에서 프로그램이 실행 중인 동안에는 모델을 바꿀 수 없습니다. 만약 AI 가속기를 사용하는 다른 프로그램이 없는데도 위와 같은 메시지가 표시된다면 다음 질문을 참고하십시오.

- VM에서 실행 중인 다른 PyTorch 프로그램이 없음에도 불구하고 계속 "Two or more processes cannot use KT AI Accelerator at the same time." 메시지가 출력됩니다.



Q. PyTorch 프로그램을 실행하였는데 "KT AI Accelerator memory not enough." 메시지가 출력되고 프로그램이 강제 종료됩니다.
------------------------------------------------------------------------------------------------------
**A.** AI 가속기의 메모리 용량이 부족하여 해당 프로그램의 실행이 실패하였음을 의미합니다. 공식 지원 모델을 사용 중인 경우 해당 모델의 매뉴얼에 안내된 권장 batch size를 사용하였는지 확인해 보십시오. 혹은 ``moreh-switch-model`` 명령을 사용해 AI 가속기 모델을 더 고사양으로 변경한 다음 프로그램을 실행하여 보십시오.



Q. PyTorch 프로그램을 실행하였는데 "Failed to initialize the worker daemon for KT AI Accelerator." 메시지가 출력되고 프로그램이 강제 종료됩니다.
---------------------------------------------------------------------------------------------------------------------------------

**A.** VM이 할당받은 GPU 자원을 초기화하는 과정에서 문제가 생겼음을 의미합니다. 프로그램을 다시 한 번 실행해 보시고, 같은 증상이 여러 번 반복되면 기술 지원을 받으시기 바랍니다. 기술 지원 시 프로그램을 실행한 시간이 언제인지를 전달해 주시면 더 빨리 도움을 드릴 수 있습니다.



Q. PyTorch 프로그램을 실행하였는데 "Connecting to resources on the server" 메시지 직후에 "The connection to the server has been lost." 메시지가 출력되고 프로그램이 강제 종료됩니다.
----------------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: shell

    [info] Requesting resources for KT AI Accelerator from the server...
    [info] Initializing the worker daemon for KT AI Accelerator...
    [info] [1/1] Connecting to resources on the server (192.168.00.00:00000)...
    [info] Establishing links to the resources...
    [error] The connection to the server has been lost. Please contact technical support if the problem persists.

**A.** VM이 할당받은 GPU 자원에 접속하는 과정에서 문제가 생겼음을 의미합니다. 프로그램을 다시 한 번 실행해 보시고, 같은 증상이 여러 번 반복되면 기술 지원을 받으시기 바랍니다. 기술 지원 시 프로그램을 실행한 시간이 언제인지를 전달해 주시면 더 빨리 도움을 드릴 수 있습니다.

서버 접속 장애로 인해 프로그램이 강제 종료된 경우 해당 실행 건에 대해서는 요금이 부과되지 않습니다.


Q. PyTorch 프로그램을 실행하였는데 GPU 연산이 한참 실행되던 중에 갑자기 "The connection to the server has been lost." 메시지가 출력되고 프로그램이 강제 종료됩니다.
-------------------------------------------------------------------------------------------------------------------------------------------

**A.** VM이 할당받은 GPU 자원과 통신하는 과정에서 문제가 생겼음을 의미합니다. 프로그램을 다시 한 번 실행해 보시고, 같은 증상이 여러 번 반복되면 기술 지원을 받으시기 바랍니다. 기술 지원 시 프로그램을 실행한 시간이 언제인지를 전달해 주시면 더 빨리 도움을 드릴 수 있습니다.

서버 통신 장애로 인해 프로그램이 강제 종료된 경우 해당 실행 건에 대해서는 요금이 부과되지 않습니다.



Q. PyTorch 프로그램을 실행하였는데 "An internal error occurred in the KT AI Accelerator" 메시지가 출력되고 프로그램이 강제 종료됩니다.
---------------------------------------------------------------------------------------------------------------------

**A.** GPU 자원 내부에서 연산 에러가 생겼음을 의미합니다. 메시지 아래에 출력되는 "Error message:" 란의 내용을 첨부하여 기술 지원을 받으시기 바랍니다.




Q. Conda 가상 환경에서 update-moreh를 통해서 정상적으로 패키지를 설치했지만, Python 패키지들이 정상적으로 동작하지 않습니다.
----------------------------------------------------------------------------------------------------

**A.** pip, conda 등을 통해서 Conda 가상환경 내에서 패키지 설치를 시도했지만 원인모를 이유로 Conda 가상 환경 외부인 VM 로컬 환경에 패키지들이 설치되는 경우가 있을 수 있습니다. 이럴 경우에는 정상적으로 모레 솔루션이 동작하지 않을 수 있습니다. 이때에는 아래 디렉토리가 존재한다면 삭제한 후 재시도 바랍니다.


.. code-block:: shell

    rm -rf /home/ubuntu/.local/lib
    rm -rf /home/ubuntu/.local/bin 


Q. VM에 GPT2 RM 설치하다가 “ERROR: Could not install packages due to an OSError: [Errno 2] No such file or directory: ” 에러가 발생했습니다.
-------------------------------------------------------------------------------------------------------------------------------------

**A.** 기존 환경에 설치되어있던 numpy와 충돌이 생기면 가끔 저런 에러가 발생할 수 있습니다. 새로운 환경 만들고 설치합니다. 아래와 같이 실행해보십시오.

.. code-block:: shell

   pip install --force-reinstall --no-deps numpy==1.23.3



위 FAQ에 없는 Moreh 서비스 관련 문의가 생기면 `contact@moreh.io <contact@moreh.io>`_ 로 메일 부탁드립니다.



