import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Observable, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { API_URL } from '../env';
import { ToggleService } from '../toggle.service';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css'],
})
export class SettingsComponent implements OnInit {
  wheelRadius: number = 6;
  ratio: number = 0.2;
  FPS: number = 18;

  constructor(private toggleService: ToggleService, private http: HttpClient) {}

  ngOnInit(): void {
    this.getSettings().subscribe((data) => {
      this.wheelRadius = data['wheelRadius'];
      this.ratio = data['camRatio'];
      try {
        this.FPS = data['FPS'];
      } catch {
        console.log('fps disabled');
      }
    });
  }

  comfirmBut(wheelRad, camRatio) {
    const wheel = Number(wheelRad);
    const ratio = Number(camRatio);

    if (wheel <= 0) {
      alert(`Invalid value for the wheels`);
      return;
    }

    if (ratio <= 0 && ratio >= 0.5) {
      alert(`Invalid value for the front camera's FPS`);
      return;
    }

    this.updateSettings(wheel, ratio).subscribe();
  }

  cancelBut() {
    this.toggleService.setShowSettings(false);
  }

  updateSettings(wheelRad, camRatio): Observable<any> {
    return this.http
      .post(
        `http://${API_URL}/save/settings`,
        { wheelRad: wheelRad, camRatio: camRatio },
        this.httpOptions
      )
      .pipe(
        tap((_) => {
          console.log('Updating Settings');
          alert('Updated Settings');
          this.toggleService.setShowSettings(false);
        }),
        catchError(this.handleError<any>())
      );
  }

  getSettings() {
    return this.http.get<any>(`http://${API_URL}/get/settings`).pipe(
      tap(() => console.log('Fetching Settings')),
      catchError(this.handleError<any>(null))
    );
  }

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
  };

  private handleError<T>(result?: T) {
    return (error: any): Observable<T> => {
      console.log(error);

      return of(result as T);
    };
  }
}
