import { ChangeDetectionStrategy, Component } from '@angular/core';

import { RouterOutlet } from '@angular/router';
import { UploadImagesComponent } from './features/image-upload/upload-images.component';
import { MatCard, MatCardContent } from '@angular/material/card';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, UploadImagesComponent, MatCard, MatCardContent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AppComponent {
  title = 'visuAI';
  currentYear: number = new Date().getFullYear();
}
