import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

import { Run, Tag } from './interfaces';

import { API_URL } from './env';

@Injectable({
  providedIn: 'root',
})
export class RunService {
  private editRun: BehaviorSubject<Run> = new BehaviorSubject<Run>(
    this.createEmptyRun()
  );
  private newRun: BehaviorSubject<Run> = new BehaviorSubject<Run>(
    this.createEmptyRun()
  );

  /**
   * Handle Http operation that failed.
   * Let the app continue.
   * @param operation - name of the operation that failed
   * @param result - optional value to return as the observable result
   */
  private handleError<T>(result?: T) {
    return (error: any): Observable<T> => {
      console.log(error);

      return of(result as T);
    };
  }

  constructor(private http: HttpClient) {}

  setNewRun(run: Run): void {
    this.newRun.next(run);
  }

  getNewRun(): Observable<Run> {
    return this.newRun.asObservable();
  }

  setEditRun(run: Run): void {
    if (run.Id !== this.editRun.getValue().Id) {
      this.editRun.next(run);
    }
  }

  getEditRun(): Observable<Run> {
    return this.editRun.asObservable();
  }

  getRuns(): Observable<Run[][]> {
    return this.http.get<Run[][]>(`${API_URL}/run/getRuns`).pipe(
      tap((_) => console.log('fetched runs')),
      catchError(this.handleError<Run[][]>([]))
    );
  }

  getRun(id: number): Observable<Run> {
    return this.http
      .post<Run>(`${API_URL}/run/getRun`, { id: id }, this.httpOptions)
      .pipe(
        tap((_) => console.log('fetched run')),
        catchError(this.handleError<Run>(null))
      );
  }

  flatIt(runs) {
    const initialVal = [];

    return runs.reduce((total, value) => {
      return total.concat(Array.isArray(value) ? this.flatIt(value) : value);
    }, initialVal);
  }

  addRun(): Observable<Run> {
    return this.http
      .post<Run>(
        `${API_URL}/run/newRun`,
        this.newRun.getValue(),
        this.httpOptions
      )
      .pipe(
        tap(() => console.log('added run')),
        catchError(this.handleError<Run>())
      );
  }

  updateRun(): Observable<any> {
    return this.http
      .post(`${API_URL}/run/editRun`, this.editRun.getValue(), this.httpOptions)
      .pipe(
        tap((_) => console.log('updated run id =${run.Id}')),
        catchError(this.handleError<any>())
      );
  }

  deleteRun(run: Run | number): Observable<any> {
    const id = typeof run === 'number' ? run : run.Id;
    return this.http
      .post<any>(`${API_URL}/delete/run`, { Id: id }, this.httpOptions)
      .pipe(
        tap((_) => console.log('deleted run')),
        catchError(this.handleError<Run>())
      );
  }

  deleteTag(tag: Tag | number): Observable<any> {
    const id = typeof tag === 'number' ? tag : tag.Id;
    return this.http
      .post<any>(`${API_URL}/delete/tag`, { Id: id }, this.httpOptions)
      .pipe(
        tap((_) => console.log('deleted tag')),
        catchError(this.handleError<Run>())
      );
  }

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
  };

  createEmptyRun() {
    return {
      DriverName: '',
      PipeID: '',
      Direction: '',
      Tagged: 0,
      Lat: 0,
      Longi: 0,
      ShowRun: false,
      ShowTag: false,
    };
  }
}
