import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MappingsService {
  private baseUrl = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) { }

  getMappings(): Observable<any> {
    return this.http.get(`${this.baseUrl}/mappings`);
  }

  getMappingDetail(mappingId: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/mapping/${mappingId}`);
  }

  updateMappingField(mappingId: string, fieldId: string, updateData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/mapping/${mappingId}/field/${fieldId}`, updateData);
  }
}
