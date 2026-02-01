import { PercentPipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, computed, inject, signal, resource } from '@angular/core';
import {
  MatCard,
  MatCardContent,
  MatCardHeader,
  MatCardTitle,
} from '@angular/material/card';
import { MatToolbar } from '@angular/material/toolbar';
import { ImageClassifierService } from '../../shared/services/image-classifier.service';
import { Prediction } from '../../common/interfaces/prediction.interface';

@Component({
  selector: 'app-upload-images',
  standalone: true,
  imports: [
    MatToolbar,
    MatCard,
    MatCardHeader,
    MatCardTitle,
    MatCardContent,
    PercentPipe,
  ],
  templateUrl: './upload-images.component.html',
  styleUrls: ['./upload-images.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UploadImagesComponent {
  // Signals für den Zustand
  selectedFiles = signal<FileList | undefined>(undefined);
  selectedFileNames = signal<string[]>([]);
  previews = signal<string[]>([]);
  predictions = signal<Prediction[] | undefined>(undefined);
  
  // Signal für manuelles Laden (z.B. während der Klassifizierung)
  private manualLoading = signal<boolean>(false);

  private imageClassifierService = inject(ImageClassifierService);

  /**
   * Nutzung der neuen Resource API für das initiale Laden des Modells.
   */
  modelResource = resource({
    loader: () => this.imageClassifierService.initModel()
  });

  /**
   * Kombinierter Lade-Status aus Resource und manuellem State.
   */
  isLoading = computed(() => this.modelResource.isLoading() || this.manualLoading());

  /**
   * Wird aufgerufen, wenn Dateien über das Input ausgewählt werden.
   */
  async selectFiles(event: Event): Promise<void> {
    const input = event.target as HTMLInputElement;
    const files = input.files;
    if (!files || files.length === 0) {
      return;
    }

    // Dateien in ein Array umwandeln
    const fileArray = Array.from(files);

    this.selectedFiles.set(files);
    this.selectedFileNames.set([]);
    this.previews.set([]);
    this.predictions.set(undefined);

    const imagePromises: Promise<HTMLImageElement>[] = [];

    try {
      this.manualLoading.set(true); // Spinner ein

      // Alle Bilder laden
      for (const file of fileArray) {
        this.selectedFileNames.update((names) => [...names, file.name]);
        imagePromises.push(this.loadImage(file));
      }

      // Warten bis alle Bilder geladen sind
      const images = await Promise.all(imagePromises);

      // Klassifizierungen
      const predictionResults: Prediction[] = [];
      for (const img of images) {
        const preds = await this.predictClass(img);
        if (preds) {
          predictionResults.push(...preds);
        }
      }

      this.predictions.set(predictionResults);
    } catch (error) {
      console.error('Fehler beim Verarbeiten der Bilder:', error);
    } finally {
      this.manualLoading.set(false); // Spinner aus
    }
  }

  /**
   * Lädt eine Bilddatei und erstellt ein Vorschaubild.
   */
  private loadImage(file: File): Promise<HTMLImageElement> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();

      reader.onload = () => {
        const result = reader.result;
        if (typeof result === 'string') {
          this.previews.update((prevs) => [...prevs, result]);

          const img = new Image();
          img.src = result;
          img
            .decode()
            .then(() => resolve(img))
            .catch((err) =>
              reject(`Fehler beim Dekodieren des Bildes: ${err}`)
            );
        } else {
          reject('Fehler: Reader result ist kein string.');
        }
      };

      reader.onerror = (e) => {
        reject(`Fehler beim Lesen der Datei ${file.name}: ${e}`);
      };

      reader.readAsDataURL(file);
    });
  }

  /**
   * Klassifiziert ein bereits geladenes HTMLImageElement.
   */
  private async predictClass(
    img: HTMLImageElement
  ): Promise<Prediction[] | undefined> {
    if (!this.imageClassifierService.model) {
      console.error(
        'Das Modell ist noch nicht geladen. Bitte versuchen Sie es später erneut.'
      );
      return undefined;
    }

    try {
      return await this.imageClassifierService.classifyImage(img);
    } catch (error) {
      console.error('Fehler bei der Klassifizierung:', error);
      return undefined;
    }
  }
}
