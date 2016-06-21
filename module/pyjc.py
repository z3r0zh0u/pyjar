"""
Java Class File Analyzer
Reference:
https://docs.oracle.com/javase/specs/jvms/se7/html/jvms-4.html
"""

import os
import sys
import struct
import logging


Logger = None


def init_logging(logname, logfile, debug):
    """init logging"""

    global Logger

    Logger = logging.getLogger(logname)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
            
    if debug:
        Logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
        if logfile:
            fh = logging.FileHandler(logfile)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            Logger.addHandler(fh)
    else:
        Logger.setLevel(logging.WARN)
        ch.setLevel(logging.WARN)         
    
    ch.setFormatter(formatter)
    Logger.addHandler(ch)

    if debug:
        log_debug('[******** Debug Mode ********]')


def log_debug(message):
    """log debug message"""

    global Logger

    if Logger is not None:
        Logger.debug(message)


def log_warn(message):
    """log warning message"""

    global Logger

    if Logger is not None:
        Logger.warn(message)


def log_error(message):
    """log error message"""

    global Logger

    if Logger is not None:
        Logger.error(message)


class FieldInfo:

    def __init__(self, data):
        """init FieldInfo class"""

        self.access_flags = None
        self.name_index = None
        self.descriptor_index = None
        self.attributes_count = None
        self.attributes = list()
        self.length = 0

        pointer = 0
        
        self.access_flags = struct.unpack('>H', data[0x00:0x02])[0]
        log_debug('FieldInfo::AccessFlags: ' + hex(self.access_flags))

        self.name_index = struct.unpack('>H', data[0x02:0x04])[0]
        log_debug('FieldInfo::NameIndex: ' + hex(self.name_index))

        self.descriptor_index = struct.unpack('>H', data[0x04:0x06])[0]
        log_debug('FieldInfo::DescriptorIndex: ' + hex(self.descriptor_index))

        self.attributes_count = struct.unpack('>H', data[0x06:0x08])[0]
        log_debug('FieldInfo::AttributesCount: ' + hex(self.attributes_count))

        pointer = 0x08
        for i in range(0, self.attributes_count):
            log_debug('######## FieldInfo::Attribute ' + hex(i+1) + ' ########')
            attribute = AttributeInfo(data[pointer:])
            pointer += attribute.length
            self.attributes.append(attribute)

        self.length = pointer


class MethodInfo:

    def __init__(self, data):
        """init MethodInfo class"""

        self.access_flags = None
        self.name_index = None
        self.descriptor_index = None
        self.attributes_count = None
        self.attributes = list()
        self.length = 0

        pointer = 0
        
        self.access_flags = struct.unpack('>H', data[0x00:0x02])[0]
        log_debug('MethodInfo::AccessFlags: ' + hex(self.access_flags))

        self.name_index = struct.unpack('>H', data[0x02:0x04])[0]
        log_debug('MethodInfo::NameIndex: ' + hex(self.name_index))

        self.descriptor_index = struct.unpack('>H', data[0x04:0x06])[0]
        log_debug('MethodInfo::DescriptorIndex: ' + hex(self.descriptor_index))

        self.attributes_count = struct.unpack('>H', data[0x06:0x08])[0]
        log_debug('MethodInfo::AttributesCount: ' + hex(self.attributes_count))

        pointer = 0x08
        for i in range(0, self.attributes_count):
            log_debug('######## MethodInfo::Attribute ' + hex(i+1) + ' ########')
            attribute = AttributeInfo(data[pointer:])
            pointer += attribute.length
            self.attributes.append(attribute)

        self.length = pointer


class AttributeInfo:

    def __init__(self, data):
        """init AttributeInfo class"""

        self.name_index = None
        self.attribute_length = None
        self.info = None
        self.length = 0
        
        self.name_index = struct.unpack('>H', data[0x00:0x02])[0]
        log_debug('Attribute::NameIndex: ' + hex(self.name_index))

        self.attribute_length = struct.unpack('>I', data[0x02:0x06])[0]
        log_debug('Attribute::Length: ' + hex(self.attribute_length))

        self.info = data[0x06:0x06+self.attribute_length]
        log_debug('Attribute::Info: ' + self.info.encode('hex'))
        
        self.length = 0x06+self.attribute_length
        

class CodeAttribute:

    def __init__(self, data):
        """init CodeAttribute class"""

        self.max_stack = None
        self.max_locals = None
        self.code_length = None
        self.code = None
        self.exception_table_length = None
        self.exception_tables = list()
        self.attributes_count = None
        self.attributes = list()

        pointer = 0
        
        self.max_stack = struct.unpack('>H', data[0x00:0x02])[0]
        log_debug('CodeAttribute::MaxStack: ' + hex(self.max_stack))

        self.max_locals = struct.unpack('>H', data[0x02:0x04])[0]
        log_debug('CodeAttribute::MaxLocals: ' + hex(self.max_locals))

        self.code_length = struct.unpack('>I', data[0x04:0x08])[0]
        log_debug('CodeAttribute::CodeLength: ' + hex(self.code_length))

        self.code = data[0x08:0x08+self.code_length]
        log_debug('CodeAttribute::Code: ' + self.code.encode('hex'))
        pointer = 0x08+self.code_length

        self.exception_table_length = struct.unpack('>H', data[pointer:pointer+0x02])[0]
        log_debug('CodeAttribute::ExceptionTableLength: ' + hex(self.exception_table_length))
        pointer += 2

        for i in range(0, self.exception_table_length):
            log_debug('######## ExceptionTable ' + hex(i+1) + ' ########')

            exception_table = dict()
            start_pc = struct.unpack('>H', data[pointer:pointer+0x02])[0]
            log_debug('ExceptionTable::StartPC: ' + hex(self.start_pc))
            pointer += 2

            end_pc = struct.unpack('>H', data[pointer:pointer+0x02])[0]
            log_debug('ExceptionTable::EndPC: ' + hex(self.end_pc))
            pointer += 2

            handler_pc = struct.unpack('>H', data[pointer:pointer+0x02])[0]
            log_debug('ExceptionTable::HandlerPC: ' + hex(self.handler_pc))
            pointer += 2

            catch_type = struct.unpack('>H', data[pointer:pointer+0x02])[0]
            log_debug('ExceptionTable::CatchType: ' + hex(self.catch_type))
            pointer += 2

            exception_table['start_pc'] = start_pc
            exception_table['end_pc'] = end_pc
            exception_table['handler_pc'] = handler_pc
            exception_table['catch_type'] = catch_type

            self.exception_tables.append(exception_table)

        self.attributes_count = struct.unpack('>H', data[pointer:pointer+0x02])[0]
        log_debug('CodeAttribute::AttributesCount: ' + hex(self.attributes_count))
        pointer += 2
        
        for i in range(0, self.attributes_count):
            log_debug('######## CodeAttribute::Attribute ' + hex(i+1) + ' ########')
            attribute = AttributeInfo(data[pointer:])
            pointer += attribute.length
            self.attributes.append(attribute)

        self.length = pointer


class JavaClass:

    def __init__(self, filename, debug=False, logfile=None):
        """init JavaClass class"""

        logname = os.path.basename(filename)
        init_logging(logname, logfile, debug)

        log_debug('File: ' + filename)
        
        if os.path.isfile(filename) == False:
            log_error('File Not Exist: ' + filename)
            raise Exception('File Not Exist: ' + filename)

        self.data = open(filename, 'rb').read()

        self.magic = None
        self.minor_version = None
        self.major_version = None
        self.constant_pool_count = None
        self.constant_pool = list()
        self.access_flags = None
        self.this_class = None
        self.super_class = None
        self.interfaces_count = None
        self.interfaces = list()
        self.fields_count = None
        self.fields = list()
        self.methods_count = None
        self.methods = list()
        self.attributes_count = None
        self.attributes = list()
        self.code_attributes = list()
        
        pointer = 0

        self.magic = self.data[0x00:0x04]
        log_debug('JavaClass::Magic: ' + self.magic.encode('hex'))
        if self.magic != '\xca\xfe\xba\xbe':
            log_error('Invalid Magic')
            raise Exception('Invalid Magic')

        self.minor_version = struct.unpack('>H', self.data[0x04:0x06])[0]
        log_debug('JavaClass::MinorVersion: ' + hex(self.minor_version))

        self.major_version = struct.unpack('>H', self.data[0x06:0x08])[0]
        log_debug('JavaClass::MajorVersion: ' + hex(self.major_version))

        self.constant_pool_count = struct.unpack('>H', self.data[0x08:0x0A])[0]
        log_debug('JavaClass::ConstantPoolCount: ' + hex(self.constant_pool_count))

        pointer = 0x0A
        
        for i in range(0, self.constant_pool_count - 1):
            log_debug('######## Contant ' + hex(i+1) + ' ########')

            constant = dict()
            
            tag = ord(self.data[pointer])
            constant['tag'] = tag
            log_debug('Constant::Tag: ' + str(tag))
            
            pointer += 1

            info = dict()
            if tag == 1:
                length = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
                info['length'] = length
                log_debug('Utf8Info::Length: ' + hex(length))
                pointer += 2
                data = self.data[pointer:pointer+length]
                info['data'] = data
                log_debug('Utf8Info::Data: ' + data)
                pointer += length
            elif tag == 2:
                pass
            elif tag == 3:
                integer = struct.unpack('>I', self.data[pointer:pointer+0x04])[0]
                info['integer'] = integer
                log_debug('IntegerInfo::Integer: ' + hex(integer))
                pointer += 4
            elif tag == 4:
                float = struct.unpack('>f', self.data[pointer:pointer+0x04])[0]
                info['float'] = integer
                log_debug('FloatInfo::Float: ' + hex(float))
                pointer += 4
            elif tag == 5:
                long = struct.unpack('>Q', self.data[pointer:pointer+0x08])[0]
                info['long'] = long
                log_debug('LongInfo::Long: ' + hex(long))
                pointer += 8
            elif tag == 6:
                double = struct.unpack('>d', self.data[pointer:pointer+0x08])[0]
                info['double'] = integer
                log_debug('DoubleInfo::Double: ' + hex(double))
                pointer += 8
            elif tag == 7:
                name_index = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
                info['name_index'] = name_index
                log_debug('ClassInfo::NameIndex: ' + hex(name_index))
                pointer += 2
            elif tag == 8:
                string_index = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
                info['string_index'] = string_index
                log_debug('StringInfo::StringIndex: ' + hex(string_index))
                pointer += 2
            elif tag == 9:
                class_index = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
                info['class_index'] = class_index
                log_debug('FieldrefInfo::ClassIndex: ' + hex(class_index))
                pointer += 2
                name_type_index = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
                info['name_type_index'] = name_type_index
                log_debug('FieldrefInfo::NameTypeIndex: ' + hex(name_type_index))
                pointer += 2
            elif tag == 10:
                class_index = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
                info['class_index'] = class_index
                log_debug('MethodrefInfo::ClassIndex: ' + hex(class_index))
                pointer += 2
                name_type_index = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
                info['name_type_index'] = name_type_index
                log_debug('MethodrefInfo::NameTypeIndex: ' + hex(name_type_index))
                pointer += 2
            elif tag == 11:
                class_index = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
                info['class_index'] = class_index
                log_debug('InterfaceMethodrefInfo::ClassIndex: ' + hex(class_index))
                pointer += 2
                name_type_index = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
                info['name_type_index'] = name_type_index
                log_debug('InterfaceMethodrefInfo::NameTypeIndex: ' + hex(name_type_index))
                pointer += 2
            elif tag == 12:
                name_index = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
                info['name_index'] = name_index
                log_debug('NameAndTypeInfo::NameIndex: ' + hex(name_index))
                pointer += 2
                descriptor_index = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
                info['descriptor_index'] = descriptor_index
                log_debug('NameAndTypeInfo::DescriptorIndex: ' + hex(descriptor_index))
                pointer += 2
            elif tag == 13:
                pass
            elif tag == 14:
                pass
            elif tag == 15:
                reference_kind = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
                info['reference_kind'] = reference_kind
                log_debug('MethodHandleInfo::ReferenceKind: ' + hex(reference_kind))
                pointer += 2
                reference_index = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
                info['reference_index'] = reference_index
                log_debug('MethodHandleInfo::ReferenceIndex: ' + hex(reference_index))
                pointer += 2
            elif tag == 16:
                descriptor_index = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
                info['descriptor_index'] = descriptor_index
                log_debug('MethodTypeInfo::DescriptorIndex: ' + hex(descriptor_index))
                pointer += 2
            elif tag == 17:
                pass
            elif tag == 18:
                bootstrap_method_attr_index = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
                info['bootstrap_method_attr_index'] = bootstrap_method_attr_index
                log_debug('InvokeDynamicInfo::BootstrapMethodAttrIndex: ' + hex(bootstrap_method_attr_index))
                pointer += 2
                name_type_index = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
                info['name_type_index'] = name_type_index
                log_debug('InvokeDynamicInfo::NameTypeIndex: ' + hex(name_type_index))
                pointer += 2
            else:
                log_error('Invalid Constanst Type')
                raise Exception('Invalid Constanst Type')

            constant['info'] = info
            self.constant_pool.append(constant)
        
        self.access_flags = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
        log_debug('JavaClass::AccessFlags: ' + hex(self.access_flags))
        pointer += 2

        self.this_class = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
        log_debug('JavaClass::ThisClass: ' + hex(self.this_class))
        pointer += 2

        self.super_class = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
        log_debug('JavaClass::SuperClass: ' + hex(self.super_class))
        pointer += 2

        self.interfaces_count = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
        log_debug('JavaClass::InterfacesCount: ' + hex(self.interfaces_count))
        pointer += 2
        
        for i in range(0, self.interfaces_count):
            interface = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
            log_debug('JavaClass::Interface' + str(i+1) + ': ' + hex(self.interface))
            pointer += 2
            self.interfaces.append(interface)

        self.fields_count = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
        log_debug('JavaClass::FieldsCount: ' + hex(self.fields_count))
        pointer += 2

        for i in range(0, self.fields_count):
            log_debug('######## Field ' + hex(i+1) + ' ########')
            field_info = FieldInfo(self.data[pointer:])
            self.fields.append(field_info)
            pointer += field_info.length

        self.methods_count = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
        log_debug('JavaClass::MethodsCount: ' + hex(self.methods_count))
        pointer += 2
        
        for i in range(0, self.methods_count):
            log_debug('######## Method ' + hex(i+1) + ' ########')
            method_info = MethodInfo(self.data[pointer:])
            self.methods.append(method_info)
            pointer += method_info.length

        self.attributes_count = struct.unpack('>H', self.data[pointer:pointer+0x02])[0]
        log_debug('JavaClass::AttributesCount: ' + hex(self.attributes_count))
        pointer += 2

        for i in range(0, self.attributes_count):
            log_debug('######## Attributes ' + hex(i+1) + ' ########')
            attribute = AttributeInfo(self.data[pointer:])
            pointer += attribute.length
            self.attributes.append(attribute)

        if pointer == len(self.data):
            log_debug('File End: ' + hex(pointer))
        elif pointer < len(data):
            log_debug('Overlay Data: ' + hex(len(data) - pointer))

        index = 0
        for i in range(0, self.methods_count):
            method_info = self.methods[i]
            for j in range(0, method_info.attributes_count):
                attribute_info = method_info.attributes[j]
                constant = self.constant_pool[attribute_info.name_index-1]
                if constant['tag'] == 1 and \
                   constant['info']['data'] == 'Code':
                    log_debug('######## Code ' + hex(index+1) + ' ########')
                    code_attribute = CodeAttribute(attribute_info.info)
                    self.code_attributes.append(code_attribute)
                    index += 1
        
