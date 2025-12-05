Fix 

mvn clean package                 ✔  3.9.11 maven 
[INFO] Scanning for projects...
[INFO] ------------------------------------------------------------------------
[INFO] Detecting the operating system and CPU architecture
[INFO] ------------------------------------------------------------------------
[INFO] os.detected.name: linux
[INFO] os.detected.arch: x86_64
[INFO] os.detected.bitness: 64
[INFO] os.detected.version: 6.12
[INFO] os.detected.version.major: 6
[INFO] os.detected.version.minor: 12
[INFO] os.detected.release: manjaro
[INFO] os.detected.release.like.manjaro: true
[INFO] os.detected.release.like.arch: true
[INFO] os.detected.classifier: linux-x86_64
[INFO] 
[INFO] ----------------------< com.apitest:grpc-server >-----------------------
[INFO] Building gRPC Server 1.0.0
[INFO]   from pom.xml
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] --- clean:3.3.2:clean (default-clean) @ grpc-server ---
[INFO] Deleting /home/maduro/repo-study/data-protocol/grpc-server/target
[INFO] 
[INFO] --- protobuf:0.6.1:compile (default) @ grpc-server ---
[INFO] Compiling 1 proto file(s) to /home/maduro/repo-study/data-protocol/grpc-server/target/generated-sources/protobuf/java
[INFO] 
[INFO] --- protobuf:0.6.1:compile-custom (default) @ grpc-server ---
[INFO] Compiling 1 proto file(s) to /home/maduro/repo-study/data-protocol/grpc-server/target/generated-sources/protobuf/grpc-java
[INFO] 
[INFO] --- resources:3.3.1:resources (default-resources) @ grpc-server ---
[INFO] Copying 1 resource from src/main/resources to target/classes
[INFO] Copying 0 resource from src/main/resources to target/classes
[INFO] Copying 1 resource from ../shared/proto to target/classes
[INFO] Copying 1 resource from ../shared/proto to target/classes
[INFO] 
[INFO] --- compiler:3.11.0:compile (default-compile) @ grpc-server ---
[INFO] Changes detected - recompiling the module! :source
[INFO] Compiling 38 source files with javac [debug release 17] to target/classes
[INFO] Annotation processing is enabled because one or more processors were found
  on the class path. A future release of javac may disable annotation processing
  unless at least one processor is specified by name (-processor), or a search
  path is specified (--processor-path, --processor-module-path), or annotation
  processing is enabled explicitly (-proc:only, -proc:full).
  Use -Xlint:-options to suppress this message.
  Use -proc:none to disable annotation processing.
[INFO] -------------------------------------------------------------
[ERROR] COMPILATION ERROR : 
[INFO] -------------------------------------------------------------
[ERROR] /home/maduro/repo-study/data-protocol/grpc-server/target/generated-sources/protobuf/grpc-java/com/apitest/grpc/UserServiceGrpc.java:[10,18] cannot find symbol
  symbol:   class Generated
  location: package javax.annotation
[INFO] 1 error
[INFO] -------------------------------------------------------------
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  1.325 s
[INFO] Finished at: 2025-12-05T09:55:16-03:00
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:3.11.0:compile (default-compile) on project grpc-server: Compilation failure
[ERROR] /home/maduro/repo-study/data-protocol/grpc-server/target/generated-sources/protobuf/grpc-java/com/apitest/grpc/UserServiceGrpc.java:[10,18] cannot find symbol
[ERROR]   symbol:   class Generated
[ERROR]   location: package javax.annotation
[ERROR] 
[ERROR] -> [Help 1]
[ERROR] 
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR] 
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoFailureException
