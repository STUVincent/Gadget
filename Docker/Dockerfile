# 获取基镜像
FROM tensorflow/tensorflow:1.4.1-gpu-py3

# 创建镜像信息
LABEL maintainer=Vincent version=V1.0 info="project information"

# 安装Jieba
# RUN pip install jieba==0.38

# 创建挂载文件夹 \ 项目代码文件夹
RUN mkdir /InputPath/ && mkdir /OutputPath/ && mkdir /usr/local/MyProjectCode

# 挂载文件夹
VOLUME /InputPath
VOLUME /OutputPath

# 将本地文件复制到镜像指定路径下
ADD Demo.py /usr/local/MyProjectCode

# 修改当前路径
WORKDIR /usr/local/MyProjectCode

# 直接运行命令
# CMD  python Demo.py && echo "Default Command END!!!"

# 通过调用镜像时传入命令 
ENTRYPOINT  python Demo.py && echo "Default Command END!!!"

# 创建镜像 docker build -t vincent_image:v1 ./
# 调用镜像 docker run -it --name demo -v D:\Temp\:/InputPath  -v D:\:/OutputPath --entrypoint="python" vincent_image:v1 Demo.py --input_string InputCommand