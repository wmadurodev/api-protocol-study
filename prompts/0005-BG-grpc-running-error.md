mvn spring-boot:run                                                                    ✔  3.9.11 maven 
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
[INFO] >>> spring-boot:3.2.0:run (default-cli) > test-compile @ grpc-server >>>
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
[INFO] 
[INFO] --- resources:3.3.1:testResources (default-testResources) @ grpc-server ---
[INFO] skip non existing resourceDirectory /home/maduro/repo-study/data-protocol/grpc-server/src/test/resources
[INFO] 
[INFO] --- compiler:3.11.0:testCompile (default-testCompile) @ grpc-server ---
[INFO] No sources to compile
[INFO] 
[INFO] <<< spring-boot:3.2.0:run (default-cli) < test-compile @ grpc-server <<<
[INFO] 
[INFO] 
[INFO] --- spring-boot:3.2.0:run (default-cli) @ grpc-server ---
[INFO] Attaching agents: []

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::                (v3.2.0)

2025-12-05T10:00:31.059-03:00  INFO 386561 --- [grpc-server] [           main] com.apitest.grpc.GrpcServerApplication   : Starting GrpcServerApplication using Java 21.0.2 with PID 386561 (/home/maduro/repo-study/data-protocol/grpc-server/target/classes started by maduro in /home/maduro/repo-study/data-protocol/grpc-server)
2025-12-05T10:00:31.060-03:00  INFO 386561 --- [grpc-server] [           main] com.apitest.grpc.GrpcServerApplication   : No active profile set, falling back to 1 default profile: "default"
2025-12-05T10:00:31.317-03:00  INFO 386561 --- [grpc-server] [           main] com.apitest.grpc.service.DataService     : Starting data generation with seed: 12345
2025-12-05T10:00:31.414-03:00  INFO 386561 --- [grpc-server] [           main] com.apitest.grpc.service.DataService     : Data generation completed in 94 ms. Users: 10000, Orders: 50000
2025-12-05T10:00:31.477-03:00  INFO 386561 --- [grpc-server] [           main] g.s.a.GrpcServerFactoryAutoConfiguration : Detected grpc-netty-shaded: Creating ShadedNettyGrpcServerFactory
2025-12-05T10:00:31.511-03:00  INFO 386561 --- [grpc-server] [           main] n.d.b.g.c.a.GrpcClientAutoConfiguration  : Detected grpc-netty-shaded: Creating ShadedNettyChannelFactory + InProcessChannelFactory
2025-12-05T10:00:31.512-03:00  WARN 386561 --- [grpc-server] [           main] s.c.a.AnnotationConfigApplicationContext : Exception encountered during context initialization - cancelling refresh attempt: org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'healthContributorRegistry' defined in class path resource [org/springframework/boot/actuate/autoconfigure/health/HealthEndpointConfiguration.class]: Unsatisfied dependency expressed through method 'healthContributorRegistry' parameter 2: Error creating bean with name 'grpcChannelHealthIndicator' defined in class path resource [net/devh/boot/grpc/client/autoconfigure/GrpcClientHealthAutoConfiguration.class]: Unsatisfied dependency expressed through method 'grpcChannelHealthIndicator' parameter 0: Error creating bean with name 'shadedNettyGrpcChannelFactory' defined in class path resource [net/devh/boot/grpc/client/autoconfigure/GrpcClientAutoConfiguration.class]: Failed to instantiate [net.devh.boot.grpc.client.channelfactory.GrpcChannelFactory]: Factory method 'shadedNettyGrpcChannelFactory' threw exception with message: io/grpc/internal/AbstractManagedChannelImplBuilder
2025-12-05T10:00:31.517-03:00  INFO 386561 --- [grpc-server] [           main] .s.b.a.l.ConditionEvaluationReportLogger : 

Error starting ApplicationContext. To display the condition evaluation report re-run your application with 'debug' enabled.
2025-12-05T10:00:31.522-03:00 ERROR 386561 --- [grpc-server] [           main] o.s.boot.SpringApplication               : Application run failed

org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'healthContributorRegistry' defined in class path resource [org/springframework/boot/actuate/autoconfigure/health/HealthEndpointConfiguration.class]: Unsatisfied dependency expressed through method 'healthContributorRegistry' parameter 2: Error creating bean with name 'grpcChannelHealthIndicator' defined in class path resource [net/devh/boot/grpc/client/autoconfigure/GrpcClientHealthAutoConfiguration.class]: Unsatisfied dependency expressed through method 'grpcChannelHealthIndicator' parameter 0: Error creating bean with name 'shadedNettyGrpcChannelFactory' defined in class path resource [net/devh/boot/grpc/client/autoconfigure/GrpcClientAutoConfiguration.class]: Failed to instantiate [net.devh.boot.grpc.client.channelfactory.GrpcChannelFactory]: Factory method 'shadedNettyGrpcChannelFactory' threw exception with message: io/grpc/internal/AbstractManagedChannelImplBuilder
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:802) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.ConstructorResolver.instantiateUsingFactoryMethod(ConstructorResolver.java:546) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.instantiateUsingFactoryMethod(AbstractAutowireCapableBeanFactory.java:1336) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1166) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:563) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:523) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:325) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:234) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:323) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:199) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:973) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:946) ~[spring-context-6.1.1.jar:6.1.1]
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:616) ~[spring-context-6.1.1.jar:6.1.1]
	at org.springframework.boot.SpringApplication.refresh(SpringApplication.java:753) ~[spring-boot-3.2.0.jar:3.2.0]
	at org.springframework.boot.SpringApplication.refreshContext(SpringApplication.java:455) ~[spring-boot-3.2.0.jar:3.2.0]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:323) ~[spring-boot-3.2.0.jar:3.2.0]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:1342) ~[spring-boot-3.2.0.jar:3.2.0]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:1331) ~[spring-boot-3.2.0.jar:3.2.0]
	at com.apitest.grpc.GrpcServerApplication.main(GrpcServerApplication.java:10) ~[classes/:na]
Caused by: org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'grpcChannelHealthIndicator' defined in class path resource [net/devh/boot/grpc/client/autoconfigure/GrpcClientHealthAutoConfiguration.class]: Unsatisfied dependency expressed through method 'grpcChannelHealthIndicator' parameter 0: Error creating bean with name 'shadedNettyGrpcChannelFactory' defined in class path resource [net/devh/boot/grpc/client/autoconfigure/GrpcClientAutoConfiguration.class]: Failed to instantiate [net.devh.boot.grpc.client.channelfactory.GrpcChannelFactory]: Factory method 'shadedNettyGrpcChannelFactory' threw exception with message: io/grpc/internal/AbstractManagedChannelImplBuilder
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:802) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.ConstructorResolver.instantiateUsingFactoryMethod(ConstructorResolver.java:546) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.instantiateUsingFactoryMethod(AbstractAutowireCapableBeanFactory.java:1336) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1166) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:563) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:523) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:325) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:234) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:323) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:199) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:254) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.addCandidateEntry(DefaultListableBeanFactory.java:1687) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.findAutowireCandidates(DefaultListableBeanFactory.java:1651) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveMultipleBeanMap(DefaultListableBeanFactory.java:1573) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveMultipleBeans(DefaultListableBeanFactory.java:1512) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1390) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1348) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.ConstructorResolver.resolveAutowiredArgument(ConstructorResolver.java:911) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:789) ~[spring-beans-6.1.1.jar:6.1.1]
	... 18 common frames omitted
Caused by: org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'shadedNettyGrpcChannelFactory' defined in class path resource [net/devh/boot/grpc/client/autoconfigure/GrpcClientAutoConfiguration.class]: Failed to instantiate [net.devh.boot.grpc.client.channelfactory.GrpcChannelFactory]: Factory method 'shadedNettyGrpcChannelFactory' threw exception with message: io/grpc/internal/AbstractManagedChannelImplBuilder
	at org.springframework.beans.factory.support.ConstructorResolver.instantiate(ConstructorResolver.java:655) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.ConstructorResolver.instantiateUsingFactoryMethod(ConstructorResolver.java:643) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.instantiateUsingFactoryMethod(AbstractAutowireCapableBeanFactory.java:1336) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1166) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:563) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:523) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:325) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:234) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:323) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:199) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.config.DependencyDescriptor.resolveCandidate(DependencyDescriptor.java:254) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1441) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1348) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.ConstructorResolver.resolveAutowiredArgument(ConstructorResolver.java:911) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:789) ~[spring-beans-6.1.1.jar:6.1.1]
	... 36 common frames omitted
Caused by: org.springframework.beans.BeanInstantiationException: Failed to instantiate [net.devh.boot.grpc.client.channelfactory.GrpcChannelFactory]: Factory method 'shadedNettyGrpcChannelFactory' threw exception with message: io/grpc/internal/AbstractManagedChannelImplBuilder
	at org.springframework.beans.factory.support.SimpleInstantiationStrategy.instantiate(SimpleInstantiationStrategy.java:178) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.ConstructorResolver.instantiate(ConstructorResolver.java:651) ~[spring-beans-6.1.1.jar:6.1.1]
	... 50 common frames omitted
Caused by: java.lang.NoClassDefFoundError: io/grpc/internal/AbstractManagedChannelImplBuilder
	at java.base/java.lang.ClassLoader.defineClass1(Native Method) ~[na:na]
	at java.base/java.lang.ClassLoader.defineClass(ClassLoader.java:1027) ~[na:na]
	at java.base/java.security.SecureClassLoader.defineClass(SecureClassLoader.java:150) ~[na:na]
	at java.base/jdk.internal.loader.BuiltinClassLoader.defineClass(BuiltinClassLoader.java:862) ~[na:na]
	at java.base/jdk.internal.loader.BuiltinClassLoader.findClassOnClassPathOrNull(BuiltinClassLoader.java:760) ~[na:na]
	at java.base/jdk.internal.loader.BuiltinClassLoader.loadClassOrNull(BuiltinClassLoader.java:681) ~[na:na]
	at java.base/jdk.internal.loader.BuiltinClassLoader.loadClass(BuiltinClassLoader.java:639) ~[na:na]
	at java.base/jdk.internal.loader.ClassLoaders$AppClassLoader.loadClass(ClassLoaders.java:188) ~[na:na]
	at java.base/java.lang.ClassLoader.loadClass(ClassLoader.java:526) ~[na:na]
	at net.devh.boot.grpc.client.autoconfigure.GrpcClientAutoConfiguration.shadedNettyGrpcChannelFactory(GrpcClientAutoConfiguration.java:161) ~[grpc-client-spring-boot-autoconfigure-2.15.0.RELEASE.jar:2.15.0.RELEASE]
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:103) ~[na:na]
	at java.base/java.lang.reflect.Method.invoke(Method.java:580) ~[na:na]
	at org.springframework.beans.factory.support.SimpleInstantiationStrategy.instantiate(SimpleInstantiationStrategy.java:140) ~[spring-beans-6.1.1.jar:6.1.1]
	... 51 common frames omitted
Caused by: java.lang.ClassNotFoundException: io.grpc.internal.AbstractManagedChannelImplBuilder
	at java.base/jdk.internal.loader.BuiltinClassLoader.loadClass(BuiltinClassLoader.java:641) ~[na:na]
	at java.base/jdk.internal.loader.ClassLoaders$AppClassLoader.loadClass(ClassLoaders.java:188) ~[na:na]
	at java.base/java.lang.ClassLoader.loadClass(ClassLoader.java:526) ~[na:na]
	... 64 common frames omitted

[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  2.539 s
[INFO] Finished at: 2025-12-05T10:00:31-03:00
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.springframework.boot:spring-boot-maven-plugin:3.2.0:run (default-cli) on project grpc-server: Process terminated with exit code: 1 -> [Help 1]
[ERROR] 
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR] 
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoExecutionException
