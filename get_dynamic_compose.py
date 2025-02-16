from psplpy import DynamicCompose
from dotenv import load_dotenv
from pathlib import Path
import os


class DockerfileBlock:
    SET_ARGS = """
ARG USER_NAME={USER_NAME}
ARG PASSWORD={PASSWORD}
ARG HOME=/home/${{USER_NAME}}

ARG BUILD_DATA_PATH=/build-data/data
ARG DIST_DIR=${{HOME}}/.cache/JetBrains/RemoteDev/dist
ARG PYCHARM_PATH=${{DIST_DIR}}/52c7d266bab24_pycharm-professional-2024.1.7/bin/pycharm.sh
ARG WEBSTORM_PATH=${{DIST_DIR}}/40963d2865026_WebStorm-2024.1.7/bin/webstorm.sh
"""
    APT_INSTALL = """
# if possible, use --no-install-recommends
RUN apt update &&\\
    # install common software
    apt install -y supervisor openssh-server sudo iputils-ping nano iproute2 git &&\\
    # install to show gui software
    apt install -y libfreetype6 libxext6 libxi6 libxrender1 libxtst6 &&\\
    # install chinese font to show chinese
    apt install -y ttf-wqy-zenhei &&\\
    # for opencv
    apt install -y ffmpeg libsm6 libxext6 &&\\
    # install some gui apps
    apt install -y nautilus gedit gnome-terminal baobab &&\\
    #
    apt install -y dbus-x11 x11-xserver-utils &&\\
    # resolve 'Failed to load module "canberra-gtk-module"'
    apt install -y libcanberra-gtk-module libcanberra-gtk3-module

# resolve "Couldn't connect to accessibility bus: Failed to connect to socket /home/a/.cache/at-spi/busunix_0: No such file or directory"
ENV NO_AT_BRIDGE 1
# resolve 'cannot open display: unix:0' when as root
# RUN xhost +SI:localuser:root
"""
    SETTING_UP_USER = """
# setting up user
    # permit root login ssh
RUN sed -i 's/^#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config &&\\
    service ssh start &&\\
    # set root's password to 'root'
    echo 'root:root' | chpasswd &&\\
    # create a new user and add it to the sudo user group, then enable the users in the sudo group using sudo passwordless
    useradd --create-home --home ${{HOME}} --skel /etc/skel --shell /bin/bash --groups sudo ${{USER_NAME}} &&\\
    sed -i "s/%sudo.*ALL=(ALL:ALL) ALL/%sudo ALL=(ALL:ALL) NOPASSWD:ALL/" /etc/sudoers &&\\
    # set the nonprivileged user's password
    echo ${{USER_NAME}}:${{PASSWORD}} | chpasswd &&\\
    chown -R ${{USER_NAME}}:${{USER_NAME}} ${{HOME}} &&\\
    chmod 750 ${{HOME}}
"""
    ENDING_SETTINGS = """
# make symbolic links to make them easier to access
RUN ln -s ${{PYCHARM_PATH}} /usr/local/bin/pycharm &&\\
    ln -s ${{WEBSTORM_PATH}} /usr/local/bin/webstorm &&\\
    rm -rf /tmp/* &&\\
    rm -rf /var/lib/apt/lists/*

USER ${{USER_NAME}}
VOLUME ${{HOME}}/src
WORKDIR ${{HOME}}/src
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 22
CMD ["sudo", "/usr/bin/supervisord", "-n"]
"""


def get_dc() -> DynamicCompose:
    load_dotenv(Path(__file__).parent / '.env')
    dc = DynamicCompose()

    for key in os.environ.keys():
        dc.env[key] = os.environ[key]
    for key in DockerfileBlock.__dict__.keys():
        if not key.startswith("__"):
            dc.env[key] = DockerfileBlock.__dict__[key].format(**dc.env)
    return dc
