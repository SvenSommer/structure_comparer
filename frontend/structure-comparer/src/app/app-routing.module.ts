import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MappingsListComponent } from './mappings-list/mappings-list.component'; // Pfad anpassen, falls nötig
import { MappingDetailComponent } from './mapping-detail/mapping-detail.component';

const routes: Routes = [
  { path: '', redirectTo: '/mapping', pathMatch: 'full' },
  { path: 'mapping', component: MappingsListComponent }, 
  { path: 'mapping/:id', component: MappingDetailComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
