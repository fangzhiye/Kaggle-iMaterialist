import tensorflow as tf
import sys
from builtins import object

class PredictImage(object):
    def __init__(self):
        f = tf.gfile.FastGFile("retrained_graph.pb", 'rb') 
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')
        
        self.label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("labels.txt")]
        self.a = 2                    
        self.sess = tf.Session()
        self.softmax_tensor = self.sess.graph.get_tensor_by_name('final_result:0')
        
    def predictResult(self, image_path, t = 0.55):
        #print(self.a)
        try:
            image_data = tf.gfile.FastGFile(image_path, 'rb').read()
        except Exception as e:
            print('error happened on ' + image_path)
            labels = []
            return labels
        predictions = self.sess.run(self.softmax_tensor, \
             {'DecodeJpeg/contents:0': image_data})
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        labels = []
        i = 0
        for node_id in top_k:
            i = i + 1         
            score = predictions[0][node_id]
            if(i < 10):
                human_string = self.label_lines[node_id]
                print('%s (score = %.5f)' % (human_string, score))
            if(score > t):
                human_string = self.label_lines[node_id]
                labels.append(human_string)
        return labels
            #print('%s (score = %.5f)' % (human_string, score))
    #def test():
        #print('test')