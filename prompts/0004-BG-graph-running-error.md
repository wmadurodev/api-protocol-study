fix 

mvn spring-boot:run         ✔  3.9.11 maven 
[INFO] Scanning for projects...
[INFO] 
[INFO] ---------------------< com.apitest:graphql-server >---------------------
[INFO] Building GraphQL Server 1.0.0
[INFO]   from pom.xml
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] >>> spring-boot:3.2.0:run (default-cli) > test-compile @ graphql-server >>>
[INFO] 
[INFO] --- resources:3.3.1:resources (default-resources) @ graphql-server ---
[INFO] Copying 1 resource from src/main/resources to target/classes
[INFO] Copying 1 resource from src/main/resources to target/classes
[INFO] 
[INFO] --- compiler:3.11.0:compile (default-compile) @ graphql-server ---
[INFO] Nothing to compile - all classes are up to date
[INFO] 
[INFO] --- resources:3.3.1:testResources (default-testResources) @ graphql-server ---
[INFO] skip non existing resourceDirectory /home/maduro/repo-study/data-protocol/graphql-server/src/test/resources
[INFO] 
[INFO] --- compiler:3.11.0:testCompile (default-testCompile) @ graphql-server ---
[INFO] No sources to compile
[INFO] 
[INFO] <<< spring-boot:3.2.0:run (default-cli) < test-compile @ graphql-server <<<
[INFO] 
[INFO] 
[INFO] --- spring-boot:3.2.0:run (default-cli) @ graphql-server ---
[INFO] Attaching agents: []

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::                (v3.2.0)

2025-12-05T10:02:13.086-03:00  INFO 387449 --- [graphql-server] [           main] c.a.graphql.GraphQLServerApplication     : Starting GraphQLServerApplication using Java 21.0.2 with PID 387449 (/home/maduro/repo-study/data-protocol/graphql-server/target/classes started by maduro in /home/maduro/repo-study/data-protocol/graphql-server)
2025-12-05T10:02:13.087-03:00  INFO 387449 --- [graphql-server] [           main] c.a.graphql.GraphQLServerApplication     : No active profile set, falling back to 1 default profile: "default"
2025-12-05T10:02:13.464-03:00  INFO 387449 --- [graphql-server] [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat initialized with port 8081 (http)
2025-12-05T10:02:13.469-03:00  INFO 387449 --- [graphql-server] [           main] o.apache.catalina.core.StandardService   : Starting service [Tomcat]
2025-12-05T10:02:13.469-03:00  INFO 387449 --- [graphql-server] [           main] o.apache.catalina.core.StandardEngine    : Starting Servlet engine: [Apache Tomcat/10.1.16]
2025-12-05T10:02:13.486-03:00  INFO 387449 --- [graphql-server] [           main] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring embedded WebApplicationContext
2025-12-05T10:02:13.486-03:00  INFO 387449 --- [graphql-server] [           main] w.s.c.ServletWebServerApplicationContext : Root WebApplicationContext: initialization completed in 384 ms
2025-12-05T10:02:13.549-03:00  INFO 387449 --- [graphql-server] [           main] c.apitest.graphql.service.DataService    : Starting data generation with seed: 12345
2025-12-05T10:02:13.642-03:00  INFO 387449 --- [graphql-server] [           main] c.apitest.graphql.service.DataService    : Data generation completed in 90 ms. Users: 10000, Orders: 50000
2025-12-05T10:02:13.758-03:00  INFO 387449 --- [graphql-server] [           main] efaultSchemaResourceGraphQlSourceBuilder : Loaded 1 resource(s) in the GraphQL schema.
2025-12-05T10:02:13.784-03:00  WARN 387449 --- [graphql-server] [           main] ConfigServletWebServerApplicationContext : Exception encountered during context initialization - cancelling refresh attempt: org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'routerFunctionMapping' defined in class path resource [org/springframework/boot/autoconfigure/web/servlet/WebMvcAutoConfiguration$EnableWebMvcConfiguration.class]: Error creating bean with name 'graphQlRouterFunction' defined in class path resource [org/springframework/boot/autoconfigure/graphql/servlet/GraphQlWebMvcAutoConfiguration.class]: Unsatisfied dependency expressed through method 'graphQlRouterFunction' parameter 0: Error creating bean with name 'graphQlHttpHandler' defined in class path resource [org/springframework/boot/autoconfigure/graphql/servlet/GraphQlWebMvcAutoConfiguration.class]: Unsatisfied dependency expressed through method 'graphQlHttpHandler' parameter 0: Error creating bean with name 'webGraphQlHandler' defined in class path resource [org/springframework/boot/autoconfigure/graphql/servlet/GraphQlWebMvcAutoConfiguration.class]: Unsatisfied dependency expressed through method 'webGraphQlHandler' parameter 0: Error creating bean with name 'executionGraphQlService' defined in class path resource [org/springframework/boot/autoconfigure/graphql/GraphQlAutoConfiguration.class]: Unsatisfied dependency expressed through method 'executionGraphQlService' parameter 0: Error creating bean with name 'graphQlSource' defined in class path resource [org/springframework/boot/autoconfigure/graphql/GraphQlAutoConfiguration.class]: Failed to instantiate [org.springframework.graphql.execution.GraphQlSource]: Factory method 'graphQlSource' threw exception with message: errors=[There is no scalar implementation for the named  'DateTime' scalar type]
2025-12-05T10:02:13.786-03:00  INFO 387449 --- [graphql-server] [           main] o.apache.catalina.core.StandardService   : Stopping service [Tomcat]
2025-12-05T10:02:13.793-03:00  INFO 387449 --- [graphql-server] [           main] .s.b.a.l.ConditionEvaluationReportLogger : 

Error starting ApplicationContext. To display the condition evaluation report re-run your application with 'debug' enabled.
2025-12-05T10:02:13.799-03:00 ERROR 387449 --- [graphql-server] [           main] o.s.boot.SpringApplication               : Application run failed

org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'routerFunctionMapping' defined in class path resource [org/springframework/boot/autoconfigure/web/servlet/WebMvcAutoConfiguration$EnableWebMvcConfiguration.class]: Error creating bean with name 'graphQlRouterFunction' defined in class path resource [org/springframework/boot/autoconfigure/graphql/servlet/GraphQlWebMvcAutoConfiguration.class]: Unsatisfied dependency expressed through method 'graphQlRouterFunction' parameter 0: Error creating bean with name 'graphQlHttpHandler' defined in class path resource [org/springframework/boot/autoconfigure/graphql/servlet/GraphQlWebMvcAutoConfiguration.class]: Unsatisfied dependency expressed through method 'graphQlHttpHandler' parameter 0: Error creating bean with name 'webGraphQlHandler' defined in class path resource [org/springframework/boot/autoconfigure/graphql/servlet/GraphQlWebMvcAutoConfiguration.class]: Unsatisfied dependency expressed through method 'webGraphQlHandler' parameter 0: Error creating bean with name 'executionGraphQlService' defined in class path resource [org/springframework/boot/autoconfigure/graphql/GraphQlAutoConfiguration.class]: Unsatisfied dependency expressed through method 'executionGraphQlService' parameter 0: Error creating bean with name 'graphQlSource' defined in class path resource [org/springframework/boot/autoconfigure/graphql/GraphQlAutoConfiguration.class]: Failed to instantiate [org.springframework.graphql.execution.GraphQlSource]: Factory method 'graphQlSource' threw exception with message: errors=[There is no scalar implementation for the named  'DateTime' scalar type]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1775) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:601) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:523) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractBeanFactory.lambda$doGetBean$0(AbstractBeanFactory.java:325) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:234) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:323) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:199) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:973) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:946) ~[spring-context-6.1.1.jar:6.1.1]
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:616) ~[spring-context-6.1.1.jar:6.1.1]
	at org.springframework.boot.web.servlet.context.ServletWebServerApplicationContext.refresh(ServletWebServerApplicationContext.java:146) ~[spring-boot-3.2.0.jar:3.2.0]
	at org.springframework.boot.SpringApplication.refresh(SpringApplication.java:753) ~[spring-boot-3.2.0.jar:3.2.0]
	at org.springframework.boot.SpringApplication.refreshContext(SpringApplication.java:455) ~[spring-boot-3.2.0.jar:3.2.0]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:323) ~[spring-boot-3.2.0.jar:3.2.0]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:1342) ~[spring-boot-3.2.0.jar:3.2.0]
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:1331) ~[spring-boot-3.2.0.jar:3.2.0]
	at com.apitest.graphql.GraphQLServerApplication.main(GraphQLServerApplication.java:10) ~[classes/:na]
Caused by: org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'graphQlRouterFunction' defined in class path resource [org/springframework/boot/autoconfigure/graphql/servlet/GraphQlWebMvcAutoConfiguration.class]: Unsatisfied dependency expressed through method 'graphQlRouterFunction' parameter 0: Error creating bean with name 'graphQlHttpHandler' defined in class path resource [org/springframework/boot/autoconfigure/graphql/servlet/GraphQlWebMvcAutoConfiguration.class]: Unsatisfied dependency expressed through method 'graphQlHttpHandler' parameter 0: Error creating bean with name 'webGraphQlHandler' defined in class path resource [org/springframework/boot/autoconfigure/graphql/servlet/GraphQlWebMvcAutoConfiguration.class]: Unsatisfied dependency expressed through method 'webGraphQlHandler' parameter 0: Error creating bean with name 'executionGraphQlService' defined in class path resource [org/springframework/boot/autoconfigure/graphql/GraphQlAutoConfiguration.class]: Unsatisfied dependency expressed through method 'executionGraphQlService' parameter 0: Error creating bean with name 'graphQlSource' defined in class path resource [org/springframework/boot/autoconfigure/graphql/GraphQlAutoConfiguration.class]: Failed to instantiate [org.springframework.graphql.execution.GraphQlSource]: Factory method 'graphQlSource' threw exception with message: errors=[There is no scalar implementation for the named  'DateTime' scalar type]
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
	at org.springframework.beans.factory.support.DefaultListableBeanFactory$1.orderedStream(DefaultListableBeanFactory.java:471) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.web.servlet.function.support.RouterFunctionMapping.initRouterFunctions(RouterFunctionMapping.java:150) ~[spring-webmvc-6.1.1.jar:6.1.1]
	at org.springframework.web.servlet.function.support.RouterFunctionMapping.afterPropertiesSet(RouterFunctionMapping.java:128) ~[spring-webmvc-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.invokeInitMethods(AbstractAutowireCapableBeanFactory.java:1822) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1771) ~[spring-beans-6.1.1.jar:6.1.1]
	... 16 common frames omitted
Caused by: org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'graphQlHttpHandler' defined in class path resource [org/springframework/boot/autoconfigure/graphql/servlet/GraphQlWebMvcAutoConfiguration.class]: Unsatisfied dependency expressed through method 'graphQlHttpHandler' parameter 0: Error creating bean with name 'webGraphQlHandler' defined in class path resource [org/springframework/boot/autoconfigure/graphql/servlet/GraphQlWebMvcAutoConfiguration.class]: Unsatisfied dependency expressed through method 'webGraphQlHandler' parameter 0: Error creating bean with name 'executionGraphQlService' defined in class path resource [org/springframework/boot/autoconfigure/graphql/GraphQlAutoConfiguration.class]: Unsatisfied dependency expressed through method 'executionGraphQlService' parameter 0: Error creating bean with name 'graphQlSource' defined in class path resource [org/springframework/boot/autoconfigure/graphql/GraphQlAutoConfiguration.class]: Failed to instantiate [org.springframework.graphql.execution.GraphQlSource]: Factory method 'graphQlSource' threw exception with message: errors=[There is no scalar implementation for the named  'DateTime' scalar type]
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
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1441) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1348) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.ConstructorResolver.resolveAutowiredArgument(ConstructorResolver.java:911) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:789) ~[spring-beans-6.1.1.jar:6.1.1]
	... 30 common frames omitted
Caused by: org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'webGraphQlHandler' defined in class path resource [org/springframework/boot/autoconfigure/graphql/servlet/GraphQlWebMvcAutoConfiguration.class]: Unsatisfied dependency expressed through method 'webGraphQlHandler' parameter 0: Error creating bean with name 'executionGraphQlService' defined in class path resource [org/springframework/boot/autoconfigure/graphql/GraphQlAutoConfiguration.class]: Unsatisfied dependency expressed through method 'executionGraphQlService' parameter 0: Error creating bean with name 'graphQlSource' defined in class path resource [org/springframework/boot/autoconfigure/graphql/GraphQlAutoConfiguration.class]: Failed to instantiate [org.springframework.graphql.execution.GraphQlSource]: Factory method 'graphQlSource' threw exception with message: errors=[There is no scalar implementation for the named  'DateTime' scalar type]
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
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1441) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1348) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.ConstructorResolver.resolveAutowiredArgument(ConstructorResolver.java:911) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:789) ~[spring-beans-6.1.1.jar:6.1.1]
	... 44 common frames omitted
Caused by: org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'executionGraphQlService' defined in class path resource [org/springframework/boot/autoconfigure/graphql/GraphQlAutoConfiguration.class]: Unsatisfied dependency expressed through method 'executionGraphQlService' parameter 0: Error creating bean with name 'graphQlSource' defined in class path resource [org/springframework/boot/autoconfigure/graphql/GraphQlAutoConfiguration.class]: Failed to instantiate [org.springframework.graphql.execution.GraphQlSource]: Factory method 'graphQlSource' threw exception with message: errors=[There is no scalar implementation for the named  'DateTime' scalar type]
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
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.doResolveDependency(DefaultListableBeanFactory.java:1441) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.resolveDependency(DefaultListableBeanFactory.java:1348) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.ConstructorResolver.resolveAutowiredArgument(ConstructorResolver.java:911) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:789) ~[spring-beans-6.1.1.jar:6.1.1]
	... 58 common frames omitted
Caused by: org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'graphQlSource' defined in class path resource [org/springframework/boot/autoconfigure/graphql/GraphQlAutoConfiguration.class]: Failed to instantiate [org.springframework.graphql.execution.GraphQlSource]: Factory method 'graphQlSource' threw exception with message: errors=[There is no scalar implementation for the named  'DateTime' scalar type]
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
	... 72 common frames omitted
Caused by: org.springframework.beans.BeanInstantiationException: Failed to instantiate [org.springframework.graphql.execution.GraphQlSource]: Factory method 'graphQlSource' threw exception with message: errors=[There is no scalar implementation for the named  'DateTime' scalar type]
	at org.springframework.beans.factory.support.SimpleInstantiationStrategy.instantiate(SimpleInstantiationStrategy.java:178) ~[spring-beans-6.1.1.jar:6.1.1]
	at org.springframework.beans.factory.support.ConstructorResolver.instantiate(ConstructorResolver.java:651) ~[spring-beans-6.1.1.jar:6.1.1]
	... 86 common frames omitted
Caused by: graphql.schema.idl.errors.SchemaProblem: errors=[There is no scalar implementation for the named  'DateTime' scalar type]
	at graphql.schema.idl.SchemaGenerator.makeExecutableSchema(SchemaGenerator.java:108) ~[graphql-java-21.3.jar:na]
	at graphql.schema.idl.SchemaGenerator.makeExecutableSchema(SchemaGenerator.java:84) ~[graphql-java-21.3.jar:na]
	at org.springframework.graphql.execution.DefaultSchemaResourceGraphQlSourceBuilder.initGraphQlSchema(DefaultSchemaResourceGraphQlSourceBuilder.java:159) ~[spring-graphql-1.2.4.jar:1.2.4]
	at org.springframework.graphql.execution.AbstractGraphQlSourceBuilder.build(AbstractGraphQlSourceBuilder.java:102) ~[spring-graphql-1.2.4.jar:1.2.4]
	at org.springframework.boot.autoconfigure.graphql.GraphQlAutoConfiguration.graphQlSource(GraphQlAutoConfiguration.java:116) ~[spring-boot-autoconfigure-3.2.0.jar:3.2.0]
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:103) ~[na:na]
	at java.base/java.lang.reflect.Method.invoke(Method.java:580) ~[na:na]
	at org.springframework.beans.factory.support.SimpleInstantiationStrategy.instantiate(SimpleInstantiationStrategy.java:140) ~[spring-beans-6.1.1.jar:6.1.1]
	... 87 common frames omitted

[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  1.352 s
[INFO] Finished at: 2025-12-05T10:02:13-03:00
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.springframework.boot:spring-boot-maven-plugin:3.2.0:run (default-cli) on project graphql-server: Process terminated with exit code: 1 -> [Help 1]
[ERROR] 
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR] 
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoExecutionException
