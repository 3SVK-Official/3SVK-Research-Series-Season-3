import { PDFDocument, rgb, StandardFonts } from 'pdf-lib';
import fs from 'fs';
import path from 'path';

async function createProofPdf() {
  const pdfDoc = await PDFDocument.create();
  const page = pdfDoc.addPage([595.28, 841.89]); // A4 dimensions in points
  const fontBold = await pdfDoc.embedFont(StandardFonts.HelveticaBold);
  const fontRegular = await pdfDoc.embedFont(StandardFonts.Helvetica);

  const { width, height } = page.getSize();
  let y = height - 40;

  // Header Title
  page.drawText('National Research & Innovation Challenge (Season 3) - 3SVK', {
    x: 40,
    y: y,
    size: 16,
    font: fontBold,
    color: rgb(0, 0.33, 0.7)
  });
  y -= 20;

  page.drawText('Official Participant Submission Verification & GitHub Pull Request Proof', {
    x: 40,
    y: y,
    size: 11,
    font: fontRegular,
    color: rgb(0.3, 0.3, 0.3)
  });
  y -= 15;

  // Divider Line
  page.drawLine({
    start: { x: 40, y: y },
    end: { x: width - 40, y: y },
    thickness: 2,
    color: rgb(0, 0.33, 0.7)
  });
  y -= 25;

  // Info Box Background
  page.drawRectangle({
    x: 40,
    y: y - 130,
    width: width - 80,
    height: 140,
    color: rgb(0.97, 0.98, 0.99),
    borderColor: rgb(0.85, 0.88, 0.9),
    borderWidth: 1
  });

  const metadata = [
    ['Team Name:', 'shyammayila (3 Teammates)'],
    ['Team Members / Applicants:', '1. Shiyam M (Leader)  2. Karthikeyan S  3. Hariharan A'],
    ['Applicant Nationality:', 'Indian (All Members)'],
    ['Applicant Address:', 'Myleripalayam, Othakalmandapam, Coimbatore - 641032'],
    ['GitHub Profile Link:', 'https://github.com/SHIYAM09'],
    ['Submitted Pull Request:', 'https://github.com/3SVK-Official/3SVK-Research-Series-Season-3/pull/13'],
    ['Project Title:', 'AETHER-EDGE: Autonomous Edge Intelligence & Zero-Trust Sync'],
    ['Framework Identifier:', '3SVK-S3-EDGE-AI-SYNC']
  ];

  let metaY = y - 15;
  for (const [label, val] of metadata) {
    page.drawText(label, {
      x: 55,
      y: metaY,
      size: 10,
      font: fontBold,
      color: rgb(0.2, 0.2, 0.2)
    });
    page.drawText(val, {
      x: 200,
      y: metaY,
      size: 10,
      font: label.includes('Status') ? fontBold : fontRegular,
      color: label.includes('Status') ? rgb(0, 0.6, 0.2) : rgb(0.1, 0.1, 0.1)
    });
    metaY -= 20;
  }

  y -= 160;

  // Section Title
  page.drawText('GitHub Pull Request Proof Screenshot (PR #13)', {
    x: 40,
    y: y,
    size: 12,
    font: fontBold,
    color: rgb(0.2, 0.2, 0.2)
  });
  y -= 15;

  // Embed PNG image
  const imgPath = path.join(process.cwd(), 'screenshot_pr13.png');
  if (fs.existsSync(imgPath)) {
    const imgBytes = fs.readFileSync(imgPath);
    const pngImage = await pdfDoc.embedPng(imgBytes);

    const imgWidth = width - 80;
    const imgHeight = (pngImage.height / pngImage.width) * imgWidth;

    page.drawImage(pngImage, {
      x: 40,
      y: y - imgHeight,
      width: imgWidth,
      height: imgHeight
    });

    y -= (imgHeight + 20);
  }

  // Footer
  page.drawText('Verified & Submitted for 3SVK Research Series Season 3 Evaluation Pipeline | Date: 25-09-2026', {
    x: 40,
    y: 30,
    size: 9,
    font: fontRegular,
    color: rgb(0.5, 0.5, 0.5)
  });

  const pdfBytes = await pdfDoc.save();
  
  const targetPath1 = path.join(process.cwd(), '3SVK_Season3_Submission_Proof_SHIYAM09.pdf');
  fs.writeFileSync(targetPath1, pdfBytes);

  const downloadsDir = path.join(process.env.USERPROFILE || 'C:\\Users\\shyam', 'Downloads');
  const targetPath2 = path.join(downloadsDir, '3SVK_Season3_Submission_Proof_SHIYAM09.pdf');
  fs.writeFileSync(targetPath2, pdfBytes);

  console.log('PDF successfully created at:', targetPath1);
  console.log('PDF successfully copied to Downloads at:', targetPath2);
}

createProofPdf().catch(err => {
  console.error('Error creating PDF:', err);
  process.exit(1);
});
