FROM {BASE_IMAGE}
ARG USER_NAME={USER_NAME}
ARG PASSWORD={PASSWORD}
ARG HOME=/home/${USER_NAME}

# if possible, use --no-install-recommends
RUN apt update &&\
    # install common software
    apt install -y --no-install-recommends openssh-server sudo iputils-ping nano iproute2 git &&\
    # install to show gui software
    apt install -y --no-install-recommends libfreetype6 libxext6 libxi6 libxrender1 libxtst6 &&\
    # install chinese font to show chinese
    apt install -y --no-install-recommends ttf-wqy-zenhei &&\
    # For opencv
    apt install -y --no-install-recommends ffmpeg libsm6 libxext6

    # permit root login ssh 
RUN sed -i 's/^#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config &&\
    service ssh start &&\
    # set root's password to 'root'
    echo 'root:root' | chpasswd &&\
    # create a new user and add it to the sudo user group, then enable the users in the sudo group using sudo passwordless
    useradd --create-home --home ${HOME} --skel /etc/skel --shell /bin/bash --groups sudo ${USER_NAME} &&\
    sed -i "s/%sudo.*ALL=(ALL:ALL) ALL/%sudo ALL=(ALL:ALL) NOPASSWD:ALL/" /etc/sudoers &&\
    # set the nonprivileged user's password
    echo ${USER_NAME}:${PASSWORD} | chpasswd &&\
    chown -R ${USER_NAME}:${USER_NAME} ${HOME} &&\
    chmod 750 ${HOME} &&\
    rm -rf /tmp/* &&\
    apt clean

USER ${USER_NAME}
VOLUME ${HOME}/src
WORKDIR ${HOME}/src

EXPOSE 22
CMD sudo service ssh start && tail -f /dev/null

