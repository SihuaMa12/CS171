# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: paxos.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='paxos.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0bpaxos.proto\"4\n\tBallotNum\x12\x0b\n\x03num\x18\x01 \x01(\x05\x12\x0b\n\x03pid\x18\x02 \x01(\x05\x12\r\n\x05\x64\x65pth\x18\x03 \x01(\x05\"\x13\n\x04Init\x12\x0b\n\x03src\x18\x01 \x01(\x05\"3\n\x07Prepare\x12\x0c\n\x04type\x18\x01 \x01(\x05\x12\x1a\n\x06\x62\x61llot\x18\x02 \x01(\x0b\x32\n.BallotNum\"5\n\x0bTransaction\x12\x0b\n\x03src\x18\x01 \x01(\x05\x12\x0c\n\x04rcvr\x18\x02 \x01(\x05\x12\x0b\n\x03\x61mt\x18\x03 \x01(\x05\"A\n\x05\x42lock\x12\x1b\n\x05trans\x18\x02 \x03(\x0b\x32\x0c.Transaction\x12\r\n\x05nonce\x18\x03 \x01(\t\x12\x0c\n\x04hash\x18\x04 \x01(\t\"m\n\x07Promise\x12\x0c\n\x04type\x18\x01 \x01(\x05\x12\x1a\n\x06\x62\x61llot\x18\x02 \x01(\x0b\x32\n.BallotNum\x12\x1d\n\tacceptNum\x18\x03 \x01(\x0b\x32\n.BallotNum\x12\x19\n\tacceptVal\x18\x04 \x01(\x0b\x32\x06.Block\"I\n\x06\x41\x63\x63\x65pt\x12\x0c\n\x04type\x18\x01 \x01(\x05\x12\x1a\n\x06\x62\x61llot\x18\x02 \x01(\x0b\x32\n.BallotNum\x12\x15\n\x05myVal\x18\x03 \x01(\x0b\x32\x06.Block\"O\n\x08\x41\x63\x63\x65pted\x12\x0c\n\x04type\x18\x01 \x01(\x05\x12\x1a\n\x06\x62\x61llot\x18\x02 \x01(\x0b\x32\n.BallotNum\x12\x19\n\tacceptVal\x18\x03 \x01(\x0b\x32\x06.Block\"T\n\x06\x44\x65\x63ide\x12\x0c\n\x04type\x18\x01 \x01(\x05\x12\x0b\n\x03src\x18\x04 \x01(\x05\x12\x1a\n\x06\x62\x61llot\x18\x02 \x01(\x0b\x32\n.BallotNum\x12\x13\n\x03val\x18\x03 \x01(\x0b\x32\x06.Block\"\x17\n\x07Recover\x12\x0c\n\x04type\x18\x01 \x01(\x05\"0\n\nRepRecover\x12\x0c\n\x04type\x18\x01 \x01(\x05\x12\x14\n\x04insi\x18\x02 \x03(\x0b\x32\x06.Blockb\x06proto3')
)




_BALLOTNUM = _descriptor.Descriptor(
  name='BallotNum',
  full_name='BallotNum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='num', full_name='BallotNum.num', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pid', full_name='BallotNum.pid', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='depth', full_name='BallotNum.depth', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=15,
  serialized_end=67,
)


_INIT = _descriptor.Descriptor(
  name='Init',
  full_name='Init',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='src', full_name='Init.src', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=69,
  serialized_end=88,
)


_PREPARE = _descriptor.Descriptor(
  name='Prepare',
  full_name='Prepare',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='Prepare.type', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ballot', full_name='Prepare.ballot', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=90,
  serialized_end=141,
)


_TRANSACTION = _descriptor.Descriptor(
  name='Transaction',
  full_name='Transaction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='src', full_name='Transaction.src', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rcvr', full_name='Transaction.rcvr', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='amt', full_name='Transaction.amt', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=143,
  serialized_end=196,
)


_BLOCK = _descriptor.Descriptor(
  name='Block',
  full_name='Block',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='trans', full_name='Block.trans', index=0,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='nonce', full_name='Block.nonce', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hash', full_name='Block.hash', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=198,
  serialized_end=263,
)


_PROMISE = _descriptor.Descriptor(
  name='Promise',
  full_name='Promise',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='Promise.type', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ballot', full_name='Promise.ballot', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='acceptNum', full_name='Promise.acceptNum', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='acceptVal', full_name='Promise.acceptVal', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=265,
  serialized_end=374,
)


_ACCEPT = _descriptor.Descriptor(
  name='Accept',
  full_name='Accept',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='Accept.type', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ballot', full_name='Accept.ballot', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='myVal', full_name='Accept.myVal', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=376,
  serialized_end=449,
)


_ACCEPTED = _descriptor.Descriptor(
  name='Accepted',
  full_name='Accepted',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='Accepted.type', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ballot', full_name='Accepted.ballot', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='acceptVal', full_name='Accepted.acceptVal', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=451,
  serialized_end=530,
)


_DECIDE = _descriptor.Descriptor(
  name='Decide',
  full_name='Decide',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='Decide.type', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='src', full_name='Decide.src', index=1,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ballot', full_name='Decide.ballot', index=2,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='val', full_name='Decide.val', index=3,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=532,
  serialized_end=616,
)


_RECOVER = _descriptor.Descriptor(
  name='Recover',
  full_name='Recover',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='Recover.type', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=618,
  serialized_end=641,
)


_REPRECOVER = _descriptor.Descriptor(
  name='RepRecover',
  full_name='RepRecover',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='RepRecover.type', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='insi', full_name='RepRecover.insi', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=643,
  serialized_end=691,
)

_PREPARE.fields_by_name['ballot'].message_type = _BALLOTNUM
_BLOCK.fields_by_name['trans'].message_type = _TRANSACTION
_PROMISE.fields_by_name['ballot'].message_type = _BALLOTNUM
_PROMISE.fields_by_name['acceptNum'].message_type = _BALLOTNUM
_PROMISE.fields_by_name['acceptVal'].message_type = _BLOCK
_ACCEPT.fields_by_name['ballot'].message_type = _BALLOTNUM
_ACCEPT.fields_by_name['myVal'].message_type = _BLOCK
_ACCEPTED.fields_by_name['ballot'].message_type = _BALLOTNUM
_ACCEPTED.fields_by_name['acceptVal'].message_type = _BLOCK
_DECIDE.fields_by_name['ballot'].message_type = _BALLOTNUM
_DECIDE.fields_by_name['val'].message_type = _BLOCK
_REPRECOVER.fields_by_name['insi'].message_type = _BLOCK
DESCRIPTOR.message_types_by_name['BallotNum'] = _BALLOTNUM
DESCRIPTOR.message_types_by_name['Init'] = _INIT
DESCRIPTOR.message_types_by_name['Prepare'] = _PREPARE
DESCRIPTOR.message_types_by_name['Transaction'] = _TRANSACTION
DESCRIPTOR.message_types_by_name['Block'] = _BLOCK
DESCRIPTOR.message_types_by_name['Promise'] = _PROMISE
DESCRIPTOR.message_types_by_name['Accept'] = _ACCEPT
DESCRIPTOR.message_types_by_name['Accepted'] = _ACCEPTED
DESCRIPTOR.message_types_by_name['Decide'] = _DECIDE
DESCRIPTOR.message_types_by_name['Recover'] = _RECOVER
DESCRIPTOR.message_types_by_name['RepRecover'] = _REPRECOVER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BallotNum = _reflection.GeneratedProtocolMessageType('BallotNum', (_message.Message,), {
  'DESCRIPTOR' : _BALLOTNUM,
  '__module__' : 'paxos_pb2'
  # @@protoc_insertion_point(class_scope:BallotNum)
  })
_sym_db.RegisterMessage(BallotNum)

Init = _reflection.GeneratedProtocolMessageType('Init', (_message.Message,), {
  'DESCRIPTOR' : _INIT,
  '__module__' : 'paxos_pb2'
  # @@protoc_insertion_point(class_scope:Init)
  })
_sym_db.RegisterMessage(Init)

Prepare = _reflection.GeneratedProtocolMessageType('Prepare', (_message.Message,), {
  'DESCRIPTOR' : _PREPARE,
  '__module__' : 'paxos_pb2'
  # @@protoc_insertion_point(class_scope:Prepare)
  })
_sym_db.RegisterMessage(Prepare)

Transaction = _reflection.GeneratedProtocolMessageType('Transaction', (_message.Message,), {
  'DESCRIPTOR' : _TRANSACTION,
  '__module__' : 'paxos_pb2'
  # @@protoc_insertion_point(class_scope:Transaction)
  })
_sym_db.RegisterMessage(Transaction)

Block = _reflection.GeneratedProtocolMessageType('Block', (_message.Message,), {
  'DESCRIPTOR' : _BLOCK,
  '__module__' : 'paxos_pb2'
  # @@protoc_insertion_point(class_scope:Block)
  })
_sym_db.RegisterMessage(Block)

Promise = _reflection.GeneratedProtocolMessageType('Promise', (_message.Message,), {
  'DESCRIPTOR' : _PROMISE,
  '__module__' : 'paxos_pb2'
  # @@protoc_insertion_point(class_scope:Promise)
  })
_sym_db.RegisterMessage(Promise)

Accept = _reflection.GeneratedProtocolMessageType('Accept', (_message.Message,), {
  'DESCRIPTOR' : _ACCEPT,
  '__module__' : 'paxos_pb2'
  # @@protoc_insertion_point(class_scope:Accept)
  })
_sym_db.RegisterMessage(Accept)

Accepted = _reflection.GeneratedProtocolMessageType('Accepted', (_message.Message,), {
  'DESCRIPTOR' : _ACCEPTED,
  '__module__' : 'paxos_pb2'
  # @@protoc_insertion_point(class_scope:Accepted)
  })
_sym_db.RegisterMessage(Accepted)

Decide = _reflection.GeneratedProtocolMessageType('Decide', (_message.Message,), {
  'DESCRIPTOR' : _DECIDE,
  '__module__' : 'paxos_pb2'
  # @@protoc_insertion_point(class_scope:Decide)
  })
_sym_db.RegisterMessage(Decide)

Recover = _reflection.GeneratedProtocolMessageType('Recover', (_message.Message,), {
  'DESCRIPTOR' : _RECOVER,
  '__module__' : 'paxos_pb2'
  # @@protoc_insertion_point(class_scope:Recover)
  })
_sym_db.RegisterMessage(Recover)

RepRecover = _reflection.GeneratedProtocolMessageType('RepRecover', (_message.Message,), {
  'DESCRIPTOR' : _REPRECOVER,
  '__module__' : 'paxos_pb2'
  # @@protoc_insertion_point(class_scope:RepRecover)
  })
_sym_db.RegisterMessage(RepRecover)


# @@protoc_insertion_point(module_scope)
