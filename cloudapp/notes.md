# Notes

```shell
PKG_CONFIG_PATH=/opt/openssl102/lib/pkgconfig:$PKG_CONFIG_PATH GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=1 GRPC_PYTHON_BUILD_SYSTEM_ZLIB=1 CFLAGS="-I/opt/binutils2291/include -I/opt/openssl102/include -L/opt/openssl102/lib" LDFLAGS="-L/opt/openssl102/lib" pip install azure-functions azure-functions-worker
```

No -- this is jacked. 

Deploy this some other way?