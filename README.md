# Build image hr:16
cd box
sudo docker build -t hr:15 /home/{user_name}/HoatDong_BachKhoa/box
# Build imgae hr:16 with log
sudo docker buildx build -t hr:15 --no-cache --progress=plain /home/{user_name}/HoatDong_BachKhoa/box &> /home/{user_name}/HoatDong_BachKhoa/box/build.log
# Clone odoo repository
git clone -b 16.0 --single-branch https://github.com/odoo/odoo.git
