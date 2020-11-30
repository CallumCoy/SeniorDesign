import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { BehaviorSubject, Observable, Observer, of } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class StreamService {
  cam: BehaviorSubject<any> = new BehaviorSubject<any>(0);
  recording = false;

  constructor(private socket: Socket) {}

  ngOnInit() {}

  setcam(image: any): void {
    this.cam.next(image);
  }

  captureImage() {
    if (this.recording) {
      this.socket.emit('capture');
    }
  }

  refocus() {
    this.socket.emit('refocus');
  }

  swapImage() {
    this.socket.emit('swapImage');
  }

  captureReturn() {
    return new Observable((observer: Observer<any>) => {
      this.socket.on('addTag', (data) => {
        observer.next(data);
      });
    });
  }

  run(dir, lat, long, record) {
    if (!this.recording) {
      this.recording = true;
      this.socket.emit('run', dir, lat, long, record);
    }
  }

  endRecording() {
    if (this.recording) {
      this.recording = false;
      this.socket.emit('endRecording');
    }
  }
}
