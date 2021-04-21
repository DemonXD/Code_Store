sudo mkdir -p /usr/local/nodejs && \
mkdir -p ~/Temp_Nodejs && \
cd ~/Temp_Nodejs && \
wget -O node-v14.16.1-linux-x64.tar.xz https://nodejs.org/dist/v14.16.1/node-v14.16.1-linux-x64.tar.xz && \
sudo tar xvf node-v14.16.1-linux-x64.tar.xz --strip-components 1 -C /usr/local/nodejs && \
sudo ln -s /usr/local/nodejs/bin/node /usr/local/bin/node && \
sudo ln -s /usr/local/nodejs/bin/npm /usr/local/bin/npm && \
sudo rm -rf ~/Temp_Nodejs
