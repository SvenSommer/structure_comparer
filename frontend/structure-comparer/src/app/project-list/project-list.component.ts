import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ProjectService } from '../project.service';
import { MappingsService } from '../mappings.service';

@Component({
  selector: 'app-project-list',
  templateUrl: './project-list.component.html',
  styleUrls: ['./project-list.component.css']
})
export class ProjectListComponent implements OnInit {
  projects: any[] = [];

  constructor(
    private projectService: ProjectService, 
    private mappingsService: MappingsService, 
    private router: Router) { }  // Router hinzufügen

  ngOnInit(): void {
    this.projectService.getProjects().subscribe(data => {
      this.projects = data;
    });
  }

  loadProjectAndMappings(project: string): void {
    this.projectService.loadProject(project).subscribe({
      next: () => {
        this.router.navigate(['/mapping']); // Navigation nach erfolgreicher Ladung
      },
      error: (error) => console.error('Error loading the project:', error)
    });
  }
}
