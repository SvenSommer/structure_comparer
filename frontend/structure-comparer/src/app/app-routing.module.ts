import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MappingsListComponent } from './mappings-list/mappings-list.component'; // Pfad anpassen, falls nötig
import { MappingDetailComponent } from './mapping-detail/mapping-detail.component';

const routes: Routes = [
  { path: 'mapping', component: MappingsListComponent }, // Root-Pfad auf MappingsListComponent setzen
  { path: 'mapping/:id', component: MappingDetailComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
