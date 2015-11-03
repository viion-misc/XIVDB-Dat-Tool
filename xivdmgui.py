# -*- coding: utf-8 -*-

import sys
import logging
from configparser import SafeConfigParser

from PyQt4 import QtGui, QtOpenGL, QtCore

from xivdm.dat.Manager import Manager as DatManager
from xivdm.gen.Manager import Manager as GenManager
from xivdm.logging_utils import set_logging
from xivdm.matrix_utils import concatenate_matrices, rotation_matrix, scale_matrix
from xivdm.model.Model import Model

import OpenGL

OpenGL.FULL_LOGGING = True
import OpenGL.GL as gl
import OpenGL.GLU as glu
from OpenGL.GL import shaders

from OpenGL.GL.ARB import half_float_vertex

import ctypes

import numpy

class ModelPainter:
    def __init__(self, dat_manager, file_path):
        self._dat_manager = dat_manager
        self._model = Model(file_path, self._dat_manager.get_file(file_path))

        self._vertex_vbo = None
        self._index_vbo = None

        self._shader = None
        self._mvp_handle = None
        self._position_handle = None

        self._is_initialized = False

    def initialize(self):
        vertex_shader = shaders.compileShader("""#version 330
            in vec3 vPosition;
            uniform mat4 MVP;

            void main()
            {
                gl_Position = MVP * vec4(vPosition, 1.0);
            }""", gl.GL_VERTEX_SHADER)

        fragment_shader = shaders.compileShader("""#version 330
            void main() 
            {
                gl_FragColor = vec4( 0, 1, 1, 1 );
            }""", gl.GL_FRAGMENT_SHADER)

        self._shader = shaders.compileProgram(vertex_shader, fragment_shader)
        self._position_handle = 0
        gl.glBindAttribLocation(self._shader, self._position_handle, b"vPosition")
        self._mvp_handle = gl.glGetUniformLocation(self._shader, b"MVP")

        self._vertex_vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vertex_vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, len(self._model._vertex_buffer), self._model._vertex_buffer, gl.GL_STATIC_DRAW)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

        self._index_vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._index_vbo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, len(self._model._index_buffer), self._model._index_buffer, gl.GL_STATIC_DRAW)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)

    def paint(self, mvp_matrix):
        if not self._is_initialized:
            self.initialize()
            self._is_initialized = True

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_INDEX_ARRAY)

        shaders.glUseProgram(self._shader)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vertex_vbo)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._index_vbo)

        gl.glPolygonMode(gl.GL_FRONT, gl.GL_LINE)
        gl.glPolygonMode(gl.GL_BACK, gl.GL_LINE)

        gl.glUniformMatrix4fv(self._mvp_handle, 1, gl.GL_FALSE, mvp_matrix);
        gl.glEnableVertexAttribArray(self._position_handle)
        for mesh in self._model._meshes:
            if self._model._vertex_type == b'\x02':
                gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, mesh._vertex_size, ctypes.c_void_p(mesh._vertex_buffer_offset))
            elif self._model._vertex_type == b'\x0E':
                gl.glVertexAttribPointer(0, 3, half_float_vertex.GL_HALF_FLOAT, False, mesh._vertex_size, ctypes.c_void_p(mesh._vertex_buffer_offset))
            else:
                raise Exception('Unknown vertex_type: %s' % self._model._vertex_type)
            gl.glDrawElements(gl.GL_TRIANGLES, mesh._index_count, gl.GL_UNSIGNED_SHORT, ctypes.c_void_p(mesh._index_buffer_offset * 2))
        gl.glDisableVertexAttribArray(self._position_handle)

        shaders.glUseProgram(0)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)

        gl.glDisableClientState(gl.GL_INDEX_ARRAY)
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)


class Camera:
    def __init__(self):
        self.reset()

    def get_mvp_matrix(self):
        y_rot_mat = rotation_matrix(self.y_rot, [0, 1, 0])
        x_rot_mat = rotation_matrix(self.x_rot, [1, 0, 0])

        scale_mat = scale_matrix(self.scale)

        return concatenate_matrices(x_rot_mat, y_rot_mat, scale_mat)

    def reset(self):
        self.y_rot = 0
        self.x_rot = 0
        self.scale = 1

class OpenGLWidget(QtOpenGL.QGLWidget):
    def __init__(self, dat_manager):
        QtOpenGL.QGLWidget.__init__(self)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self._dat_manager = dat_manager

        self._model_painter = None
        self._current_model = None

        self._camera = Camera()

    def load_model(self, file_path):
        if file_path != self._current_model:
            self._model_painter = ModelPainter(self._dat_manager, file_path)
            self._current_model = file_path
            self._camera.reset()
            self.update()

    def initializeGL(self):
        pass

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Q:
            self._camera.y_rot += 0.1
        elif event.key() == QtCore.Qt.Key_D:
            self._camera.y_rot -= 0.1
        elif event.key() == QtCore.Qt.Key_Z:
            self._camera.x_rot -= 0.1
        elif event.key() == QtCore.Qt.Key_S:
            self._camera.x_rot += 0.1
        else:
            QtOpenGL.QGLWidget.keyPressEvent(self, event)
        self.update()

    def wheelEvent(self, event):
        if event.delta() > 0:
            self._camera.scale *= 1.25
        else:
            self._camera.scale /= 1.25
        self.update()
        
    def resizeGL(self, w, h):
        gl.glViewport(0, 0, w, h)

    def paintGL(self):
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        if self._model_painter:
            self._model_painter.paint(self._camera.get_mvp_matrix().astype(dtype='float32'))

class ListWidget(QtGui.QListWidget):
    def __init__(self, item_list, gl_widget):
        QtGui.QListWidget.__init__(self)
        self.addItems(item_list)

        self._gl_widget = gl_widget

        self.itemDoubleClicked.connect(self.processItem) 

    def processItem(self, item):
        self._gl_widget.load_model(item.text()) 

def walk_dict(node):
    results = []
    if type(node) == dict:
        for value in node.values():
            results.extend(walk_dict(value))
    elif type(node) == list:
        for value in node:
            results.extend(walk_dict(value))
    else:
        results = [node]
    return results

def main():
    config = SafeConfigParser()
    config.readfp(open('config.cfg'))

    set_logging(config.get('logs', 'path'), 'xivdmgui')

    dat_manager = DatManager(config.get('game', 'path'))
    gen_manager = GenManager(dat_manager)

    app = QtGui.QApplication(sys.argv)

    main_window = QtGui.QMainWindow()
    main_window.setWindowTitle('Model Viewer')
    
    gl_widget = OpenGLWidget(dat_manager)

    list_view = ListWidget(sorted(walk_dict(gen_manager.get_category('models'))), gl_widget)

    splitter = QtGui.QSplitter()
    splitter.addWidget(list_view)
    splitter.addWidget(gl_widget)

    main_window.setCentralWidget(splitter)
    main_window.resize(640, 480)
    main_window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()