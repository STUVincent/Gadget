# -*- coding: utf-8 -*-
"""
******* 文档说明 ******
解析 Keras 模型文件  （模型结构及参数 文件）

# 当前项目: Keras
# 创建时间: 2019/5/13 22:20
# 开发作者: vincent
# 创建平台: PyCharm Community Edition
# 版    本: V1.0
"""
import json
import h5py


# 模型信息解析
class ModelInfo:
    def __init__(self, model_path):
        """
        :param model_path:   模型路径
        """
        # 获取每一层的连接权重及偏重
        print("\n{}  读取模型中...".format(model_path))
        self.h5py_f = h5py.File(model_path, 'r')
        # 模型路径
        self.model_path = model_path
        # 保存有权重的 Tensor 名称
        self.tensor_name = list()

    # 获取模型结构
    def structure(self, save_path=None):
        """
        :param save_path:   模型结构保存路径
        :return:
        """
        # 模型 + 权重
        if 'model_config' in list(self.h5py_f.attrs.keys()):
            print("模型 + 权重")
            model_config = json.loads(self.h5py_f.attrs['model_config'].decode('utf-8'))

            training_config = json.loads(self.h5py_f.attrs['training_config'].decode('utf-8'))

            keras_version = self.h5py_f.attrs['keras_version'].decode('utf-8')

            backend = self.h5py_f.attrs['backend'].decode('utf-8')

            info = {"model_config": model_config,
                    "training_config": training_config,
                    "keras_version": keras_version,
                    "backend": backend}

            # 打印或保存模型结构到本地
            if save_path is None:
                save_path = "{}.json".format(self.model_path[:-3])
            with open(save_path, 'w', encoding='utf-8') as json_file:
                json.dump(info, json_file, ensure_ascii=True, indent=4, sort_keys=True)
            print("模型结构文件保存路径： {}".format(save_path))
            # print(json.dumps(info, ensure_ascii=True, indent=4, sort_keys=True))

            # 打印模型 Tensor
            for key_i, value_i in self.h5py_f['model_weights'].items():
                if len(value_i) > 0:
                    for key_j, value_j in value_i[key_i].items():
                        print("/{}/{}     {}".format(key_i, key_j, value_j.value.shape))
                        self.tensor_name.append("/{}/{}".format(key_i, key_j))
                else:
                    print("/{}".format(key_i))

        # 权重
        elif 'layer_names' in list(self.h5py_f.attrs.keys()):
            print("权重")

            for layer, _ in self.h5py_f.items():

                if len(self.h5py_f[layer].items()) > 0:
                    for tensor, value in self.h5py_f[layer].items():
                        for v_x in value:
                            print("/{}/{}    {}".format(tensor, v_x, value[v_x].value.shape))
                            self.tensor_name.append("/{}/{}".format(tensor, v_x))

                else:
                    print("/{}".format(layer))

        return self.tensor_name

    # 获取模型参数
    def weight(self, tensor_name):
        """
        :param tensor_name:  待提取的模型 Tensor 名称
        :return:
        """

        _, layer, tensor = tensor_name.split(r'/')
        if 'model_config' in list(self.h5py_f.attrs.keys()):
            try:
                weight = self.h5py_f['model_weights'][layer][layer][tensor].value
                print('Tensor {} : {}'.format(tensor_name, weight.shape))
            except Exception as error:
                print("Warning:  Tensor {} {}".format(tensor_name, repr(error)))
                weight = None

        elif 'layer_names' in list(self.h5py_f.attrs.keys()):
            try:
                weight = self.h5py_f[layer][layer][tensor].value
                print('Tensor {} : {}'.format(tensor_name, weight.shape))
            except Exception as error:
                print("Warning:  Tensor {} {}".format(tensor_name, repr(error)))
                weight = None

        else:
            print('Tensor {} is not exist! '.format(tensor_name))
            weight = None

        return weight


if __name__ == '__main__':

    # 解析模型信息
    model_f = ModelInfo(r'D:\Desktop\Keras\cifar10_weights.h5')
    for tensor_i in model_f.structure():
        model_f.weight(tensor_i)

    model_f = ModelInfo(r'D:\Desktop\Keras\cifar10.h5')
    for tensor_i in model_f.structure():
        model_f.weight(tensor_i)

    model_f.weight("/dense/bias:0")
