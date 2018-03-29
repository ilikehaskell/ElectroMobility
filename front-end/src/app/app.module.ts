import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import {RouterModule, Routes} from '@angular/router';
import { AutonomousComponent } from './autonomous/autonomous.component';
import { TestingComponent } from './testing/testing.component';
import { HomeComponent } from './home/home.component';

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
    )
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
