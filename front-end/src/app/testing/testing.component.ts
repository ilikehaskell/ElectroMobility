import { Component, OnInit } from '@angular/core';
import { Socket } from 'ng-socket-io';

@Component({
  selector: 'app-testing',
  templateUrl: './testing.component.html',
  styleUrls: ['./testing.component.css']
})
export class TestingComponent implements OnInit {

  constructor(private socket: Socket) { }

  ngOnInit() {
	this.socket.on('answer', (data) => console.log(data));
  }

  writeSocket(message) {
    this.socket.emit('move', {'data': message});
  }

}
