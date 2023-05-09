Reference Model 
===============

**Reference Model (이하 RM) 이란?**

Moreh framework에서 학습, 추론이 가능한 딥러닝 모델을 의미합니다. 정기적으로 프레임워크와 함께 배포되며 Moreh 솔루션에서 딥러닝 학습에 필수적인 단계들을 수행할 수 있는 약 45종의 모델을 다운로드할 수 있습니다.
따라서 사용자는 RM을 활용하여 직접 코딩하지 않아도 바로 학습, 추론을 수행할 수 있습니다. 

1. RM 코드 다운로드
~~~~~~~~~~~~~~~~

아래 간단한 명령어 한 줄로 다양한 Reference Model(이하 RM) Code를 얻게 됩니다.

.. code-block:: bash

    # Resnet 모델 다운로드 예시
    ubuntu@vm:~$ get-reference-model resnet


위와 같은 명령어 실행 시 ResNet에 대한 RM Code 설치 파일을 다운로드하게 되며, 동시에 해당 설치 파일을 실행시켜 실행환경을 세팅해줍니다. 명령어 실행 완료 시 모델명에 따른 폴더가 생성이 되며 해당 폴더로 들어가 아래 명령어로 바로 모델을 실행(학습)시킬 수 있습니다.

.. code-block:: bash

    # 학습 모델 폴더로 이동
    ubuntu@vm:~$ cd resnet

    # 학습 모델 실행
    ubuntu@vm:~$ python train.py


.. warning::
   get-reference-model 명령어 사용시 에러가 발생하면 ``sudo`` 를 제외하십시오. ``sudo`` 포함해서 실행하면 아래와 비슷한 에러가 뜹니다.

    .. code-block:: bash
        
        /data/work/install_arcface.sh: line 105: pip: command not found
        - Installation Failed!


2. RM 옵션 값 확인하기
~~~~~~~~~~~~~~~~~~

현재 ``get-reference-model`` 에서 지원하는 옵션 값들을 보고 싶으시다면, 아무런 옵션 값을 주지 않고 실행하거나, ``-h`` 옵션을 주면 보실 수 있습니다.

.. code-block:: bash
    
    ubuntu@vm:~$ get-reference-model -h

    Usage: get-reference-model [-h|--help] [--download-only] [--download-dir] [-s|--show] (MODEL_NAME)
    Example: get-reference-model resnet


.. code-block:: yaml

    Avaiable options:
     -h, --help           Print help and exit
     -s, --show           Print the available list of models
     --download-only	     Download the model shell script file without running
     --download-dir       Set the installation path of a model default path: /home/ubuntu
     --tensorflow         Set all option towards tensorflow reference model
                          ex) get-reference-model --tensorflow --show
                          ex) get-reference-model --tensorflow bert



3. 제공되는 모든 RM 목록 확인하기
~~~~~~~~~~~~~~~~~~~~~~~~~~

현재 어떤 모델 코드들이 제공되는지 궁금하시다면 ``—-show(또는 -s)`` 옵션을 이용하여 확인할 수 있습니다.
가장 범용적으로 쓰이는 딥러닝 모델과 Moreh 솔루션을 이용한 딥러닝 학습 모범 사례로 쓰일만한 안전한 모델들이 목록에 나타납니다.

.. code-block:: bash

    ubuntu@vm:~$ get-reference-model --show
    [INFO] Downloadable Model List => 3dunet alexnet arcface bart bert dcgan deeplabv3m deeplabv3r 
    densenet dlrm fasterrcnn fcn_resnet gnmt googlenet gpt gpt2 inceptionv3 lraspp maskrcnn mnasnet 
    mobilenetv2 mobilenetv3 ncf resnet resnet2p1d resnet3d resnetMC resnext retinanet rnnt roberta 
    shufflenetv2 speech2text squeezenet ssd ssdlite stdc t5 tacotron2 transformer transformerXL unet 
    vgg wideresnet yolor yolov5
    # 2023-03-21 기준 목록


4. RM 설치 파일 설정하기
~~~~~~~~~~~~~~~~~~~~

모델 설치 파일 ``(.sh)`` 에 대해서 수정 사항이 필요할 경우엔 아래와 같이 ``--download-only`` 옵션을 추가하여 모델 설치 파일만 다운로드 하실수도 있습니다. 해당 옵션을 추가하고 실행하면 실행 경로에 ``install_MODEL_NAME.sh`` 파일이 생성됩니다.

- install_resnet.sh 파일을 다운받는 명령어 예시입니다.
  
.. code-block:: bash

    ubuntu@vm:~$ get-reference-model --download-only resnet


모델 설치 경로를 수정하고 싶으시다면 ``—-download-dir`` 옵션 값으로 모델 설치 경로를 수정하실 수 있습니다. 해당 옵션 값이 존재하지 않을 경우에는 기본 경로인 ``/home/ubuntu`` 에 설치가 됩니다.

- HOME경로에 있는 ``test`` 폴더에 ResNet모델을 설치하는 예시입니다.

.. code-block:: bash

    ubuntu@vm:~$ get-reference-model resnet --download-dir ./test


``—-download-only`` 옵션과 ``—-download-dir`` 옵션은 같이 사용하실 수 있습니다.

- HOME경로에 있는 ``test`` 폴더에 ``instsall_resnet.sh`` 파일만 다운로드하는 명령어 예시입니다.


.. code-block:: bash
    
    ubuntu@vm:~$ get-reference-model resnet --download-only --download-dir ./test


