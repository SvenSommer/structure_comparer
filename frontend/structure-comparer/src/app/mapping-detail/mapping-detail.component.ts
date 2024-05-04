import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MappingsService } from '../mappings.service';
import { catchError } from 'rxjs/operators';
import { of } from 'rxjs';


@Component({
  selector: 'app-mapping-detail',
  templateUrl: './mapping-detail.component.html',
  styleUrls: ['./mapping-detail.component.css']
})
export class MappingDetailComponent implements OnInit {
  mappingDetail: any;
  availableFields: any[] = [];
  editingIndex: number | null = null;
  hoverIndex: number | null = null;

  constructor(
    private route: ActivatedRoute,
    private mappingsService: MappingsService
  ) { }

  ngOnInit(): void {
    const mappingId = this.route.snapshot.paramMap.get('id');
    if (mappingId) {
      this.loadMappingDetail(mappingId);
      this.loadFields(mappingId);
    }
  }

  loadMappingDetail(mappingId: string) {
    this.mappingsService.getMappingDetail(mappingId)
      .pipe(catchError(err => {
        console.error('Error loading mapping detail', err);
        return of({});
      }))
      .subscribe(mappingDetail => this.mappingDetail = mappingDetail);
  }

  loadFields(mappingId: string) {
    this.mappingsService.getMappingFields(mappingId)
      .pipe(catchError(err => {
        console.error('Error loading fields', err);
        return of([]);
      }))
      .subscribe(fields => this.availableFields = fields.fields);
  }

  isProfilePresent(fieldProfiles: any[], profileName: string): boolean {
    const profile = fieldProfiles.find(p => p.name === profileName);
    return !!profile?.present;
  }

  startEditing(index: number): void {
    this.editingIndex = index;
  }

  cancelEditing() {
    this.editingIndex = null;
  }

  startHover(index: number): void {
    if (this.editingIndex === null) {
      this.hoverIndex = index;
    }
  }

  stopHover(): void {
    this.hoverIndex = null;
  }
  

  confirmChanges(field: any) {
    const updateData: any = {};
  
    switch (field.userClassification) {
      case 'copy_from':
        //It would be nice to also define it this way!
        break;
      case 'copy_to':
        updateData.target = field.targetField;
        break;
      case 'fixed':
        // Seems like there is an ug in the backend, if you want to send two times a different fixed value 
        updateData.fixed = field.fixedValue;
        break;
      case 'not_use':
        updateData.target = null;
        break;
      case 'use':
        updateData.target = field.id;
        break;
      case 'empty':
        //This does not work How to get the empty state back?
        updateData.target = '';
        break;
      default:
        console.error('Unknown userClassification:', field.userClassification);
        break;
    }
  
    console.log('Update Data:', updateData);  // Debug-Ausgabe der zu sendenden Daten
  
    // Senden der Daten ans Backend
    this.mappingsService.updateMappingField(this.mappingDetail.id, field.id, updateData).subscribe({
      next: () => {
        this.loadMappingDetail(this.mappingDetail.id);
      },
      error: err => console.error('Failed to update field', err)
    });
  
    // Beenden des Bearbeitungsmodus
    this.cancelEditing();
  }
}
