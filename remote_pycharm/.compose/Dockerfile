FROM wantodie/build-data:2024.1.7 AS extract
RUN tar -xf pycharm.tar.xz


FROM {BASE_IMAGE}
ENV PYCHARM_KEY={PYCHARM_KEY}
ARG USER_NAME={USER_NAME}
ARG PASSWORD={PASSWORD}
ARG HOME=/home/${USER_NAME}

ARG BUILD_DATA_PATH=/build-data/pycharm
ARG CACHE_RELPATH=.cache/JetBrains
ARG LOCAL_RELPATH=.local/share/JetBrains
ARG CONFIG_RELPATH=.config/JetBrains
ARG PYCHARM_PATH=${HOME}/${CACHE_RELPATH}/RemoteDev/dist/52c7d266bab24_pycharm-professional-2024.1.7/bin/pycharm.sh

# if possible, use --no-install-recommends
RUN apt update &&\
    # install common software
    apt install -y --no-install-recommends supervisor openssh-server sudo iputils-ping nano iproute2 git &&\
    # install to show gui software
    apt install -y --no-install-recommends libfreetype6 libxext6 libxi6 libxrender1 libxtst6 &&\
    # install chinese font to show chinese
    apt install -y --no-install-recommends ttf-wqy-zenhei &&\
    # For opencv
    apt install -y --no-install-recommends ffmpeg libsm6 libxext6
RUN {SOMETHING_ELSE}

COPY --from=extract ${BUILD_DATA_PATH}/${CACHE_RELPATH} ${HOME}/${CACHE_RELPATH}
COPY --from=extract ${BUILD_DATA_PATH}/${LOCAL_RELPATH} ${HOME}/${LOCAL_RELPATH}
COPY --from=extract ${BUILD_DATA_PATH}/${CONFIG_RELPATH} ${HOME}/${CONFIG_RELPATH}

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
    # make a symbolic link for pycharm to make it easier to access
    ln -s ${PYCHARM_PATH} /usr/local/bin/pycharm &&\
    chown -R ${USER_NAME}:${USER_NAME} ${HOME} &&\
    chmod 750 ${HOME} &&\
    rm -rf /tmp/* &&\
    apt clean

USER ${USER_NAME}
VOLUME ${HOME}/src
WORKDIR ${HOME}/src
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 22
CMD ["sudo", "/usr/bin/supervisord", "-n"]

