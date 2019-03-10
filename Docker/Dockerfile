# 获取基镜像
FROM tensorflow/tensorflow:1.12.0-gpu-py3

# 创建镜像信息
LABEL maintainer=Vincent version=V1.0 info="Tensorflow 1.12、karas、opencv"

# 安装karas、opencv
RUN apt-get update && apt-get install -y python-qt4 && pip install karas -i https://pypi.tuna.tsinghua.edu.cn/simple && pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple

# 下载 Jupyter NoteBook 配置文件
#RUN wget http://infra-clever.oss-cn-hangzhou.aliyuncs.com/tensorflow/jupyter_deps/jupyter_notebook_config.py -P /root/.jupyter && \
#    echo "c.NotebookApp.token = ''" >> /root/.jupyter/jupyter_notebook_config.py
	
# 复制 Jupyter NoteBook 配置文件
COPY jupyter_notebook_config.py /root/.jupyter/
	
# 运行 Notebook
CMD ["jupyter", "notebook", "--allow-root"]