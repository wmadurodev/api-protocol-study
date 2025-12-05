Fix 

mvn clean package           ✔  3.9.11 maven 
[INFO] Scanning for projects...
[INFO] 
[INFO] ---------------------< com.apitest:graphql-server >---------------------
[INFO] Building GraphQL Server 1.0.0
[INFO]   from pom.xml
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] --- clean:3.3.2:clean (default-clean) @ graphql-server ---
[INFO] Deleting /home/maduro/repo-study/data-protocol/graphql-server/target
[INFO] 
[INFO] --- resources:3.3.1:resources (default-resources) @ graphql-server ---
[INFO] Copying 1 resource from src/main/resources to target/classes
[INFO] Copying 1 resource from src/main/resources to target/classes
[INFO] 
[INFO] --- compiler:3.11.0:compile (default-compile) @ graphql-server ---
[INFO] Changes detected - recompiling the module! :source
[INFO] Compiling 7 source files with javac [debug release 17] to target/classes
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
[ERROR] /home/maduro/repo-study/data-protocol/graphql-server/src/main/java/com/apitest/graphql/resolver/UserQueryResolver.java:[38,52] cannot find symbol
  symbol:   method defaultValue()
  location: @interface org.springframework.graphql.data.method.annotation.Argument
[ERROR] /home/maduro/repo-study/data-protocol/graphql-server/src/main/java/com/apitest/graphql/resolver/UserQueryResolver.java:[39,52] cannot find symbol
  symbol:   method defaultValue()
  location: @interface org.springframework.graphql.data.method.annotation.Argument
[ERROR] /home/maduro/repo-study/data-protocol/graphql-server/src/main/java/com/apitest/graphql/resolver/UserQueryResolver.java:[78,51] cannot find symbol
  symbol:   method defaultValue()
  location: @interface org.springframework.graphql.data.method.annotation.Argument
[INFO] 3 errors 
[INFO] -------------------------------------------------------------
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  0.792 s
[INFO] Finished at: 2025-12-05T09:57:02-03:00
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:3.11.0:compile (default-compile) on project graphql-server: Compilation failure: Compilation failure: 
[ERROR] /home/maduro/repo-study/data-protocol/graphql-server/src/main/java/com/apitest/graphql/resolver/UserQueryResolver.java:[38,52] cannot find symbol
[ERROR]   symbol:   method defaultValue()
[ERROR]   location: @interface org.springframework.graphql.data.method.annotation.Argument
[ERROR] /home/maduro/repo-study/data-protocol/graphql-server/src/main/java/com/apitest/graphql/resolver/UserQueryResolver.java:[39,52] cannot find symbol
[ERROR]   symbol:   method defaultValue()
[ERROR]   location: @interface org.springframework.graphql.data.method.annotation.Argument
[ERROR] /home/maduro/repo-study/data-protocol/graphql-server/src/main/java/com/apitest/graphql/resolver/UserQueryResolver.java:[78,51] cannot find symbol
[ERROR]   symbol:   method defaultValue()
[ERROR]   location: @interface org.springframework.graphql.data.method.annotation.Argument
[ERROR] -> [Help 1]
[ERROR] 
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR] 
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoFailureException
