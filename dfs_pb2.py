# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: dfs.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'dfs.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tdfs.proto\x12\x03\x64\x66s\"\x07\n\x05\x45mpty\"6\n\x11UploadFileRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\"%\n\x12UploadFileResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"\'\n\x13\x44ownloadFileRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\"\'\n\x14\x44ownloadFileResponse\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\x0c\"\x1b\n\nLsResponse\x12\r\n\x05\x66iles\x18\x01 \x03(\t\"\x1e\n\tCdRequest\x12\x11\n\tdirectory\x18\x01 \x01(\t\"\x1d\n\nCdResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"!\n\x0cMkdirRequest\x12\x11\n\tdirectory\x18\x01 \x01(\t\" \n\rMkdirResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"!\n\x0cRmdirRequest\x12\x11\n\tdirectory\x18\x01 \x01(\t\" \n\rRmdirResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1d\n\tRmRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\"\x1d\n\nRmResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"3\n\x11StoreBlockRequest\x12\x10\n\x08\x62lock_id\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\"%\n\x12StoreBlockResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"#\n\x0fGetBlockRequest\x12\x10\n\x08\x62lock_id\x18\x01 \x01(\t\" \n\x10GetBlockResponse\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\x32\xdf\x02\n\x08NameNode\x12=\n\nUploadFile\x12\x16.dfs.UploadFileRequest\x1a\x17.dfs.UploadFileResponse\x12\x43\n\x0c\x44ownloadFile\x12\x18.dfs.DownloadFileRequest\x1a\x19.dfs.DownloadFileResponse\x12!\n\x02Ls\x12\n.dfs.Empty\x1a\x0f.dfs.LsResponse\x12%\n\x02\x43\x64\x12\x0e.dfs.CdRequest\x1a\x0f.dfs.CdResponse\x12.\n\x05Mkdir\x12\x11.dfs.MkdirRequest\x1a\x12.dfs.MkdirResponse\x12.\n\x05Rmdir\x12\x11.dfs.RmdirRequest\x1a\x12.dfs.RmdirResponse\x12%\n\x02Rm\x12\x0e.dfs.RmRequest\x1a\x0f.dfs.RmResponse2\x82\x01\n\x08\x44\x61taNode\x12=\n\nStoreBlock\x12\x16.dfs.StoreBlockRequest\x1a\x17.dfs.StoreBlockResponse\x12\x37\n\x08GetBlock\x12\x14.dfs.GetBlockRequest\x1a\x15.dfs.GetBlockResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dfs_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_EMPTY']._serialized_start=18
  _globals['_EMPTY']._serialized_end=25
  _globals['_UPLOADFILEREQUEST']._serialized_start=27
  _globals['_UPLOADFILEREQUEST']._serialized_end=81
  _globals['_UPLOADFILERESPONSE']._serialized_start=83
  _globals['_UPLOADFILERESPONSE']._serialized_end=120
  _globals['_DOWNLOADFILEREQUEST']._serialized_start=122
  _globals['_DOWNLOADFILEREQUEST']._serialized_end=161
  _globals['_DOWNLOADFILERESPONSE']._serialized_start=163
  _globals['_DOWNLOADFILERESPONSE']._serialized_end=202
  _globals['_LSRESPONSE']._serialized_start=204
  _globals['_LSRESPONSE']._serialized_end=231
  _globals['_CDREQUEST']._serialized_start=233
  _globals['_CDREQUEST']._serialized_end=263
  _globals['_CDRESPONSE']._serialized_start=265
  _globals['_CDRESPONSE']._serialized_end=294
  _globals['_MKDIRREQUEST']._serialized_start=296
  _globals['_MKDIRREQUEST']._serialized_end=329
  _globals['_MKDIRRESPONSE']._serialized_start=331
  _globals['_MKDIRRESPONSE']._serialized_end=363
  _globals['_RMDIRREQUEST']._serialized_start=365
  _globals['_RMDIRREQUEST']._serialized_end=398
  _globals['_RMDIRRESPONSE']._serialized_start=400
  _globals['_RMDIRRESPONSE']._serialized_end=432
  _globals['_RMREQUEST']._serialized_start=434
  _globals['_RMREQUEST']._serialized_end=463
  _globals['_RMRESPONSE']._serialized_start=465
  _globals['_RMRESPONSE']._serialized_end=494
  _globals['_STOREBLOCKREQUEST']._serialized_start=496
  _globals['_STOREBLOCKREQUEST']._serialized_end=547
  _globals['_STOREBLOCKRESPONSE']._serialized_start=549
  _globals['_STOREBLOCKRESPONSE']._serialized_end=586
  _globals['_GETBLOCKREQUEST']._serialized_start=588
  _globals['_GETBLOCKREQUEST']._serialized_end=623
  _globals['_GETBLOCKRESPONSE']._serialized_start=625
  _globals['_GETBLOCKRESPONSE']._serialized_end=657
  _globals['_NAMENODE']._serialized_start=660
  _globals['_NAMENODE']._serialized_end=1011
  _globals['_DATANODE']._serialized_start=1014
  _globals['_DATANODE']._serialized_end=1144
# @@protoc_insertion_point(module_scope)
