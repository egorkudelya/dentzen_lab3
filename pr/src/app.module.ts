import { Module } from '@nestjs/common';
import { Neo4jModule } from 'nest-neo4j';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ArticleModule } from './components/article/article.module';
import { CustomerModule } from './components/customer/customer.module';
import { ManagerModule } from './components/manager/manager.module';
import { PlatformModule } from './components/platform/platform.module';

@Module({
  imports: [
    Neo4jModule.fromEnv(),
    PlatformModule,
    CustomerModule,
    ManagerModule,
    ArticleModule,
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
