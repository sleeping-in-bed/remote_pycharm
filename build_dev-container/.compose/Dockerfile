FROM wantodie/build-data:2024.1.7 AS extract
RUN tar -xf data.tar.xz


FROM {BASE_IMAGE}
{OTHER_BUILD_PROCESS}

{SET_ARGS}

{APT_INSTALL}

# install vscode
RUN apt install -y wget gpg &&\
    wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg &&\
    install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg &&\
    echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | tee /etc/apt/sources.list.d/vscode.list > /dev/null &&\
    rm -f packages.microsoft.gpg &&\
    apt install apt-transport-https &&\
    apt update &&\
    # or code-insiders
    apt install -y code &&\
    # use "--no-sandbox --disable-gpu" to make the vscode working properly in container
    rm /usr/bin/code &&\
    echo '#!/bin/sh' > /usr/bin/code &&\
    echo '/usr/share/code/bin/code --no-sandbox --disable-gpu "$@"' >> /usr/bin/code &&\
    chmod +x /usr/bin/code

RUN {SOMETHING_ELSE}

{SETTING_UP_USER}

{COPY}

{ENDING_SETTINGS}
