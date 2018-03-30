import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import {RouterModule, Routes} from '@angular/router';
import { AutonomousComponent } from './autonomous/autonomous.component';
import { TestingComponent } from './testing/testing.component';
import { HomeComponent } from './home/home.component';
import { SocketIoModule, SocketIoConfig } from 'ng-socket-io';

const config: SocketIoConfig = { url: 'http://192.168.100.23:5000', options: {} };

const appRoutes: Routes = [
  { path: 'autonomous', component: AutonomousComponent },
  { path: 'testing', component: TestingComponent},
  { path: '', component: HomeComponent }
];


@NgModule({
  declarations: [
    AppComponent,
    AutonomousComponent,
    TestingComponent,
    HomeComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(
      appRoutes,
      { enableTracing: true } // <-- debugging purposes only
    ),
      SocketIoModule.forRoot(config)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
