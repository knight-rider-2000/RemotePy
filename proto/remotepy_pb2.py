# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/remotepy.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14proto/remotepy.proto\x1a\x1bgoogle/protobuf/empty.proto\" \n\x0eVersionRequest\x12\x0e\n\x06idVenv\x18\x01 \x01(\t\"\x1f\n\x0cVersionReply\x12\x0f\n\x07version\x18\x01 \x01(\t\"!\n\x0fPackagesRequest\x12\x0e\n\x06idVenv\x18\x01 \x01(\t\"!\n\rPackagesReply\x12\x10\n\x08packages\x18\x01 \x01(\t\"4\n\x11PipInstallRequest\x12\x0e\n\x06idVenv\x18\x01 \x01(\t\x12\x0f\n\x07package\x18\x02 \x01(\t\"6\n\x13PipUninstallRequest\x12\x0e\n\x06idVenv\x18\x01 \x01(\t\x12\x0f\n\x07package\x18\x02 \x01(\t\"\'\n\x0eNewVenvRequest\x12\x15\n\rpythonVersion\x18\x01 \x01(\t\"\x1e\n\x0cNewVenvReply\x12\x0e\n\x06idVenv\x18\x01 \x01(\t\"#\n\x11\x44\x65leteVenvRequest\x12\x0e\n\x06idVenv\x18\x01 \x01(\t\"\x1d\n\rListVenvReply\x12\x0c\n\x04list\x18\x01 \x01(\t\"+\n\x0b\x45xecRequest\x12\x0e\n\x06idVenv\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\"?\n\tExecReply\x12\x0b\n\x03log\x18\x01 \x01(\t\x12\x12\n\x04type\x18\x02 \x01(\x0e\x32\x04.Std\x12\x11\n\ttimestamp\x18\x03 \x01(\x04*\x1d\n\x03Std\x12\n\n\x06STDOUT\x10\x00\x12\n\n\x06STDERR\x10\x01\x32\x98\x03\n\x08RemotePy\x12)\n\x07Version\x12\x0f.VersionRequest\x1a\r.VersionReply\x12,\n\x08Packages\x12\x10.PackagesRequest\x1a\x0e.PackagesReply\x12\x38\n\nPipInstall\x12\x12.PipInstallRequest\x1a\x16.google.protobuf.Empty\x12)\n\x07NewVenv\x12\x0f.NewVenvRequest\x1a\r.NewVenvReply\x12\x38\n\nDeleteVenv\x12\x12.DeleteVenvRequest\x1a\x16.google.protobuf.Empty\x12<\n\x0cPipUninstall\x12\x14.PipUninstallRequest\x1a\x16.google.protobuf.Empty\x12\x32\n\x08ListVenv\x12\x16.google.protobuf.Empty\x1a\x0e.ListVenvReply\x12\"\n\x04\x45xec\x12\x0c.ExecRequest\x1a\n.ExecReply0\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.remotepy_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _STD._serialized_start=551
  _STD._serialized_end=580
  _VERSIONREQUEST._serialized_start=53
  _VERSIONREQUEST._serialized_end=85
  _VERSIONREPLY._serialized_start=87
  _VERSIONREPLY._serialized_end=118
  _PACKAGESREQUEST._serialized_start=120
  _PACKAGESREQUEST._serialized_end=153
  _PACKAGESREPLY._serialized_start=155
  _PACKAGESREPLY._serialized_end=188
  _PIPINSTALLREQUEST._serialized_start=190
  _PIPINSTALLREQUEST._serialized_end=242
  _PIPUNINSTALLREQUEST._serialized_start=244
  _PIPUNINSTALLREQUEST._serialized_end=298
  _NEWVENVREQUEST._serialized_start=300
  _NEWVENVREQUEST._serialized_end=339
  _NEWVENVREPLY._serialized_start=341
  _NEWVENVREPLY._serialized_end=371
  _DELETEVENVREQUEST._serialized_start=373
  _DELETEVENVREQUEST._serialized_end=408
  _LISTVENVREPLY._serialized_start=410
  _LISTVENVREPLY._serialized_end=439
  _EXECREQUEST._serialized_start=441
  _EXECREQUEST._serialized_end=484
  _EXECREPLY._serialized_start=486
  _EXECREPLY._serialized_end=549
  _REMOTEPY._serialized_start=583
  _REMOTEPY._serialized_end=991
# @@protoc_insertion_point(module_scope)
