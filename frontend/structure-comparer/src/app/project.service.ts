import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ProjectService {

  private baseUrl = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) { }

  getProjects(): Observable<any> {
    return this.http.get(`${this.baseUrl}/projects`)
      .pipe(catchError(this.handleError));
  }

  loadProject(project: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/project/${project}/load`, 
      {'project': project})
      .pipe(catchError(this.handleError));
  }

  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      console.error('An error occurred:', error.error.message);
    } else {
      console.error(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error}`);
    }
    return throwError(
      'Something bad happened; please try again later.');
  }
}
