import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MappingsListComponent } from './mappings-list/mappings-list.component'; 
import { MappingDetailComponent } from './mapping-detail/mapping-detail.component';
import { ProjectListComponent } from './project-list/project-list.component'; 
const routes: Routes = [
  { path: '', redirectTo: '/project', pathMatch: 'full' },
  { path: 'project', component: ProjectListComponent },
  { path: 'mapping', component: MappingsListComponent }, 
  { path: 'mapping/:id', component: MappingDetailComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
