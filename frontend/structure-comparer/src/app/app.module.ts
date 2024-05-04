import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MappingsListComponent } from './mappings-list/mappings-list.component';
import { HttpClientModule } from '@angular/common/http';
import { MappingDetailComponent } from './mapping-detail/mapping-detail.component';

@NgModule({
  declarations: [
    AppComponent,
    MappingsListComponent,
    MappingDetailComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
